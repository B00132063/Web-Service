with open("README.txt", "w") as f:
    f.write("Inventory API\n\nEndpoints:\n")
    f.write("/getAll - returns all products\n")
    f.write("/getSingleProduct - returns one product\n")

print("README created")