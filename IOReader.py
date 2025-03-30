def TryExtractTextLines(textFilepath):
    try:
        with open(textFilepath, "r", encoding="utf-8") as textIoStream:
            textLines = textIoStream.readlines()

            return textLines
    except:
        print("Could not open file")

        return None