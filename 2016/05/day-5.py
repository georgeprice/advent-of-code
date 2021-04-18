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


if __name__ == "__main__":
    door_id = input("Enter door id: ")
    p = create_password(door_id, 8)
    print(p)
