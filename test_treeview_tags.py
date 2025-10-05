import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview Tag Priority Test")

tree = ttk.Treeview(root, columns=('col1', 'col2'), show='tree headings')
tree.pack(fill='both', expand=True)

tree.heading('#0', text='ID')
tree.heading('col1', text='Name')
tree.heading('col2', text='Status')

# Configure tags - order matters!
tree.tag_configure('red', background='#ffcccc')
tree.tag_configure('green', background='#ccffcc')
tree.tag_configure('highlight', background='#ffff00')  # Yellow - configured last

# Insert items with different tag combinations
tree.insert('', 'end', text='1', values=('Item 1', 'Red only'), tags=('red',))
tree.insert('', 'end', text='2', values=('Item 2', 'Green only'), tags=('green',))
tree.insert('', 'end', text='3', values=('Item 3', 'Highlight first, then red'), tags=('highlight', 'red'))
tree.insert('', 'end', text='4', values=('Item 4', 'Red first, then highlight'), tags=('red', 'highlight'))
tree.insert('', 'end', text='5', values=('Item 5', 'Green first, then highlight'), tags=('green', 'highlight'))

print("Tag order in items:")
for i, item_id in enumerate(tree.get_children(), 1):
    tags = tree.item(item_id, 'tags')
    print(f"Item {i}: tags = {tags}")

root.mainloop()
