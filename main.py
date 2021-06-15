from random import randrange, randint, sample
import math


def serial_test(X, k):  ### k - длинна комбинации

    if len(X) % k != 0:
        N = int((len(X) / k) - len(X) % k)  ###количество непересекающихся серий
    else:
        N = int(len(X) / k)  ###количество непересекающихся серий

    static = {}
    Y = []
    for n in range(N):
        Y.append([])
        Z = ""
        for i in range(n * k, (n + 1) * k):
            Z += str(X[i])
        Y[n] = Z

    for n in range(N):
        if Y[n] in static.keys():
            static[Y[n]] = static[Y[n]] + 1
        else:
            static[Y[n]] = 1

    T = N / 2 ** k
    Hi = 0.0
    v = [k for k in static.values()]

    for i in range(2 ** k):
        Hi += ((v[i] - T) ** 2) / T

    return Hi


def correlation_test(X, k):
    N = len(X)
    m1 = m2 = M1 = M2 = M = 0

    for i in range(N - k):  # мат ожидание
        m1 += 1 / (N - k) * X[i]
        m2 += 1 / (N - k) * X[k + i]
        M1 += 1 / (N - k) * X[i] ** 2
        M2 += 1 / (N - k) * X[k + i] ** 2

    for i in range(N - k):
        M += 1 / (N + k) * (X[i] - m1) * (X[k + i] - m2)

    D1 = M1 - m1 ** 2
    D2 = M2 - m2 ** 2

    R = M / (math.sqrt(D1 * D2))
    print('R = ', R)

    Rcrit = 1 / (N - 1) + 2 / (N - 2) * math.sqrt(N * (N - 3) / (N + 1))
    print('R critical = ', Rcrit)
    print('_____________________________________')


def used_digit_generator():  ###генерация регистров
    used_digits_table = {0: [31, 3], 1: [71, 7], 2: [145, 52], 3: [55, 24], 4: [31, 6], 5: [93, 2], 6: [161, 18],
                         7: [58, 19], 8: [31, 7], 9: [137, 21], 10: [521, 32], 11: [57, 7], 12: [33, 13], 13: [35, 2],
                         14: [47, 5], 15: [52, 49]}
    used_digits_num = randrange(0, len(used_digits_table.keys()))
    used_digits = used_digits_table[used_digits_num]
    register_len = used_digits[0]
    used_digit = used_digits[1]
    return used_digit, register_len


def m_function(X, used_digit):  ###м-функция
    y = X[len(X) - 1] ^ X[used_digit]
    return (y)


def feedback(X, register_len, used_digit):  ###один шаг обратной связи X-последовательность на регистрах
    y = m_function(X, used_digit)
    for i in range(1, register_len):
        out = X[0]
        X[i - 1] = X[i]
        # X=X<<0b1
    X[register_len - 1] = y
    return X, out


def key_generator(n, register_len, l, k, used_digit):  ###генерирование ключа n-длинны
    # X = key_word
    key = []
    X = []
    for i in range(register_len):
        X.append(randint(0, 1))

    key_txt = ''.join(str(e) for e in X)
    print('key:', key_txt)
    with open('key.txt', mode='w') as file:
        file.write(key_txt)

    for i in range(n):
        X, out = feedback(X, register_len, used_digit)
        X.append(out)
        key.append(out)

    print("key's Hi=", serial_test(key, l))
    correlation_test(X, k)

    return X


def encrypt(text, key, l, k):
    print("text:", text)
    key = list(map(int, key))
    text = list(map(int, text))  # text-бинарный текст

    print("text's Hi=", serial_test(text, l))
    correlation_test(text, k)
    encrypted_text = []
    for litter, code in zip(text, key):
        encrypted_text.append(litter ^ code)

    enc_txt = ''.join(str(e) for e in encrypted_text)
    print("encrypted_text:", enc_txt)
    print("enc_text's Hi=", serial_test(encrypted_text, l))
    correlation_test(encrypted_text, k)

    with open('encrypted_text.txt', mode='w') as file:
        file.write(enc_txt)

    return encrypted_text


def decrypt(encrypted_text, key):
    decrypted_text = []
    key = list(map(int, key))

    for liter, code in zip(encrypted_text, key):
        decrypted_text.append(liter ^ code)

    ###########

    decrypted_text = ''.join(map(str, decrypted_text))
    n = int(decrypted_text, 2)
    # print(n)

    ###########

    decrypt = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    print("decrypt:", decrypt)
    with open('decrypted.txt', mode='w') as file:
        file.write(decrypt)

    return str(decrypt)


if __name__ == '__main__':
    used_digit, register_len = used_digit_generator()
    print("Введите требуемую длинну ключа:")
    n = int(input())
    print("Введите длинну анализируемой последовательности [2,3,4]:")
    l = int(input())
    print("Введите параметр К:")
    k = int(input())

    key = key_generator(n, register_len, l, k, used_digit)
    ##M-последв

    with open('text.txt') as file:
        input_text = file.readline()
        bin_text = bin(int.from_bytes(input_text.encode(), 'big'))[2:]

    encrypted_text = encrypt(bin_text, key, l, k)
    decrypted_text = decrypt(encrypted_text, key)
