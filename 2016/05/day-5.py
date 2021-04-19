import hashlib


def create_password(seed: str, length: int) -> str:
    password, suffix = "", -1
    for i in range(length):
        combined_hash = "11111"
        while combined_hash[:5] != "00000":
            suffix += 1
            combined = seed + "{}".format(suffix)
            combined_hash = hashlib.md5(str.encode(combined)).hexdigest()
        password += "{}".format(combined_hash[5])
    return password


def create_advanced_password(seed: str, length: int) -> str:
    password, suffix = ["-" for _ in range(length)], -1
    while "-" in password:
        combined_hash = "11111"
        while combined_hash[:5] != "00000":
            suffix += 1
            combined = seed + "{}".format(suffix)
            combined_hash = hashlib.md5(str.encode(combined)).hexdigest()
        position, injected = combined_hash[5], combined_hash[6]
        if position not in "0123456789":
            print(" > [attempt: {}][fail] position {} is non-numeric".format(suffix, position))
            continue
        position = int(position)
        if position >= len(password):
            print(" > [attempt: {}][fail] position {} is out of range".format(suffix, position))
        elif password[position] != "-":
            print(" > [attempt: {}][fail] position {} has been assigned to {} already".format(suffix, position,
                                                                                              password[position]))
        else:
            password[position] = injected
            print(" > [attempt: {}][success] updated position {} to {}"
                  "\n\tgot password: {}".format(suffix, position, injected, "".join(password)))
    return "".join(password)


if __name__ == "__main__":
    door_id = input("Enter door id: ")
    p = create_password(door_id, 8)
    print(p)
