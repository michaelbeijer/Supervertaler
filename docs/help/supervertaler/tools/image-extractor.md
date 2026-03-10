# Image Extractor (Superimage)

The Image Extractor pulls embedded images out of DOCX files and saves them as numbered PNG files. It also includes a built-in preview so you can quickly review what was extracted.

## Where to find it

- **Tools → Image Extractor (Superimage)...**
- Or: **Project resources** → **🎯 Image Context** (the Image Extractor lives in the bottom section of that tab)

## Extract images from a DOCX

1. Add input files:
	- **📄 Add File** to pick DOCX files
	- **📁 Folder** to add all DOCX files from a folder
2. Choose an output strategy:
	- Enable **📁 Auto-folder** to create an `Images` folder next to each DOCX
	- Or set a single output directory in the **Output directory** field
3. Set **Prefix** (default `Fig.`).
4. Click **🖼️ Extract Images**.
5. Use **📂 Extracted Files (click to preview)** to preview images.

## Using extracted images as AI context

If you also use **Image Context**, you can load a folder of figures so Supervertaler can attach relevant images automatically during AI translation (for example when the text references “Figure 2A”).

{% hint style="info" %}
Image Extractor is about getting the images out of DOCX. Image Context is about feeding those images into AI translation when needed.
{% endhint %}
