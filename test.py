import aspose.words as aw

#  Create document object
doc = aw.Document()

# Create a document builder object
builder = aw.DocumentBuilder(doc)

# Load and insert PNG image
shape = builder.insert_image("map.png")

# Specify image save format as SVG
saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)

# Save image as SVG
shape.get_shape_renderer().save("map.svg", saveOptions)