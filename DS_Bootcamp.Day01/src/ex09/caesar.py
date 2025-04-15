import sys


def caesar_cipher(text, shift, encode=True):
    result = ''
    shift_amount = shift if encode else -shift
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift_amount) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
        else:
            result += char
    return result


def main():
    if len(sys.argv) != 4:
        raise Exception('Wrong usage')

    action = sys.argv[1]
    text = sys.argv[2]
    shift = int(sys.argv[3])

    if any('\n' in c for c in text):
        raise Exception('This language is not supported')

    if action == 'encode':
        print(caesar_cipher(text, shift, encode=True))
    elif action == 'decode':
        print(caesar_cipher(text, shift, encode=False))
    else:
        raise Exception('Wrong action')


if __name__ == '__main__':
    main()