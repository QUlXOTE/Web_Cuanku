data = {
    "nama" : ["rendi", "ayah", "hakim", "rajep"],
    "kelas" : ["tinggi", "rendah", "sedang"]
}

print(data["nama"])
jumlah = int(input("banyak data yg diinput (int)= "))
for _ in range(1, jumlah+1):
    nama = input("masukan datanya = ")
    data["nama"].append(nama)
print(data["nama"])