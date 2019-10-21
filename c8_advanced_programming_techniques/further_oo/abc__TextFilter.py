import abc


# interface

# The TextFilter ABC provides no functionality at all; it exists purely to define
# an interface, in this case an is_transformer read-only property and a __call__()
# method, that all its subclasses must provide.
class TextFilter(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def is_tranformer(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self):
        raise NotImplementedError()


class CharCounter(TextFilter):
    @property
    def is_tranformer(self):
        return False

    def __call__(self, text, chars):
        count = 0
        for c in text:
            if c in chars:
                count += 1
        return count


class RunLengthEncoder(TextFilter):
    @property
    def is_tranformer(self):
        return True

    def __call__(self, utf8_string):
        byte = None
        count = 0
        binary = bytearray()
        for b in utf8_string.encode("utf8"):
            if byte is None:
                if b == 0:
                    binary.extend((0, 1, 0))
                else:
                    byte = b
                    count = 1
            else:
                if byte == b:
                    count += 1
                    if count == 255:
                        binary.extend((0, count, b))
                        byte = None
                        count = 0
                else:
                    if count == 1:
                        binary.append(byte)
                    elif count == 2:
                        binary.extend((byte, byte))
                    elif count > 2:
                        binary.extend((0, count, byte))
                    if b == 0:
                        binary.extend((0, 1, 0))
                        byte = None
                        count = 0
                    else:
                        byte = b
                        count = 1
        if count == 1:
            binary.append(byte)
        elif count == 2:
            binary.extend((byte, byte))
        elif count > 2:
            binary.extend((0, count, byte))
        return bytes(binary)


class RunLengthDecoder(TextFilter):
    @property
    def is_tranformer(self):
        return True

    def __call__(self, rle_bytes):
        binary = bytearray()
        length = None
        for b in rle_bytes:
            if length == 0:
                length = b
            elif length is not None:
                binary.extend([b for x in range(length)])
                length = None
            elif b == 0:
                length = 0
            else:
                binary.append(b)
                length = None
        if length:
            binary.extend([b for x in range(length)])
        return binary.decode("utf8")


if __name__ == '__main__':
    vowel_counter = CharCounter()
    count = vowel_counter('dog fish and cat fish', 'aeiou')
    print(count)

    print('=' * 100)
    text = 'Hack Chyson ======================= Hello hellooooooooooooooooooooooooooooooo'
    rle_encoder = RunLengthEncoder()
    rle_text = rle_encoder(text)
    print(rle_text)
    rle_decoder = RunLengthDecoder()
    original_text = rle_decoder(rle_text)
    assert text == original_text
