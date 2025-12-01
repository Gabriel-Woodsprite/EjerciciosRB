# dht11_gpiozero.py
# A gpiozero-style wrapper for DHT11 using lgpio (works on Raspberry Pi 5).
# Usage:
#   from dht11_gpiozero import DHT11Device
#   s = DHT11Device(4)   # GPIO4 (BCM)
#   print(s.temperature, s.humidity)
#   s.when_updated = lambda dev: print("updated", dev.temperature, dev.humidity)

import threading
import time
import lgpio

class DHT11Device:
    """
    Simple DHT11 wrapper using lgpio.
    Polls in background every poll_interval seconds.
    Exposes .temperature (°C) and .humidity (%) and .when_updated callback.
    """

    def __init__(self, pin=4, poll_interval=2.0, chip=0, retries=3):
        self.pin = int(pin)
        self.poll_interval = float(poll_interval)
        self.chip = int(chip)
        self._stop = threading.Event()
        self._thread = None
        self._lock = threading.RLock()
        self.temperature = None
        self.humidity = None
        self.retries = int(retries)

        # callback called after every successful read (or after any attempt)
        # assign like: sensor.when_updated = lambda dev: ...
        self.when_updated = None

        # start background polling
        self._start()

    def _start(self):
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def close(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)

    # low level read using lgpio pulses sampling
    def _single_read(self):
        """
        Return (humidity, temperature) or (None, None) on failure.
        This function performs the DHT11 handshake and samples the data line.
        """
        try:
            h = lgpio.gpiochip_open(self.chip)
        except Exception as e:
            # Could not open gpio chip
            return None, None

        try:
            # Drive pin low for >18 ms
            lgpio.gpio_claim_output(h, self.pin)
            lgpio.gpio_write(h, self.pin, 0)
            time.sleep(0.02)  # 20 ms

            # Pull high for 20-40 us
            lgpio.gpio_write(h, self.pin, 1)
            time.sleep(0.00004)  # 40 us

            # Switch to input
            lgpio.gpio_claim_input(h, self.pin)

            # Read pulses - record consecutive identical samples counts
            # We sample many times and collapse runs into pulse lengths.
            samples = []
            max_samples = 5000
            # sample as fast as possible
            for _ in range(max_samples):
                samples.append(lgpio.gpio_read(h, self.pin))

            # close chip
            lgpio.gpiochip_close(h)
        except Exception:
            try:
                lgpio.gpiochip_close(h)
            except Exception:
                pass
            return None, None

        # Convert samples to run-length encoding counts
        runs = []
        if not samples:
            return None, None
        cnt = 1
        for i in range(1, len(samples)):
            if samples[i] == samples[i-1]:
                cnt += 1
            else:
                runs.append((samples[i-1], cnt))
                cnt = 1
        runs.append((samples[-1], cnt))

        # We expect a pattern: initial response low/high, then 40 bits as high pulses lengths
        # Find longer high pulses to decode bits. This heuristic works reasonably for DHT11.
        # Build list of high-run lengths after initial preamble
        highs = [length for (val, length) in runs if val == 1]

        # Need enough high pulses for 40 bits; if not, fail
        if len(highs) < 80 // 2:  # heuristic lower bound
            return None, None

        # Heuristic: skip the first few high runs corresponding to ACK/preamble.
        # Choose a threshold by median of candidate bit high lengths.
        # Use the last 40 high-run lengths (should correspond to 40 bits if available)
        # We'll take the last 80 runs to be safe and then examine alternating pairs.
        candidate = highs[-80:] if len(highs) >= 80 else highs
        if len(candidate) < 40:
            # not enough
            return None, None

        # To decode, examine lengths of the high pulses: short -> 0, long -> 1
        # Compute a threshold between short and long by clustering (median of small half)
        sorted_candidate = sorted(candidate)
        mid = len(sorted_candidate)//2
        threshold = (sorted_candidate[mid] + sorted_candidate[max(0, mid-1)]) / 2.0

        # create bits by comparing to threshold
        bits = []
        for length in candidate:
            bits.append(1 if length > threshold else 0)
            if len(bits) == 40:
                break
        if len(bits) < 40:
            return None, None

        # convert bits to bytes
        try:
            b = bits
            humidity = int("".join(str(bit) for bit in b[0:8]), 2)
            humidity_decimal = int("".join(str(bit) for bit in b[8:16]), 2)
            temperature = int("".join(str(bit) for bit in b[16:24]), 2)
            temperature_decimal = int("".join(str(bit) for bit in b[24:32]), 2)
            checksum = int("".join(str(bit) for bit in b[32:40]), 2)
        except Exception:
            return None, None

        calc = (humidity + humidity_decimal + temperature + temperature_decimal) & 0xFF
        if calc != checksum:
            return None, None

        return humidity, temperature

    def read(self):
        """Try reading multiple times and return (humidity, temperature) or (None,None)."""
        for _ in range(self.retries):
            h, t = self._single_read()
            if h is not None:
                return h, t
            time.sleep(0.2)
        return None, None

    def _worker(self):
        while not self._stop.is_set():
            h, t = self.read()
            with self._lock:
                self.humidity = h
                self.temperature = t
            # call callback regardless (user can ignore None values)
            try:
                if callable(self.when_updated):
                    self.when_updated(self)
            except Exception:
                pass
            # sleep poll interval
            for _ in range(int(self.poll_interval*10)):
                if self._stop.is_set():
                    break
                time.sleep(0.1)

    # context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
