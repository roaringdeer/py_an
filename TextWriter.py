def go(content: str, file_dir: str = "log.txt"):
    f = open(file_dir, "w+")
    f.write(content)
    f.close()
