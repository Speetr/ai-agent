from functions.get_files_info import get_files_info

def main():
    print("Result for current directory:")
    print(f"{get_files_info("calculator", ".")}")
    print("\n")
    print("Result for 'pkg' directory:")
    print(f"{get_files_info("calculator", "pkg")}")
    print("\n")
    print("Result for '/bin' directory:")
    print(f"{get_files_info("calculator", "/bin")}")
    print("\n")
    print("Result for '../' directory:")
    print(f"{get_files_info("calculator", "../")}")

if __name__ == "__main__":
    main()