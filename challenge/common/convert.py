class Covert:
    def __init__(self):
        self.base64 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def encode_to_base64(self, num):
        if num == 0:
            return self.base64[0]

        arr = []
        while num:
            num, rem = divmod(num, len(self.base64))
            arr.append(self.base64[rem])
        arr.reverse()
        return ''.join(arr)

    def decode_from_base64(self, string):
        strlen = len(string)
        num = 0
        idx = 0
        for char in string:
            power = (strlen - (idx + 1))
            num += self.base64.index(char) * (len(self.base64) ** power)
            idx += 1
        return num
