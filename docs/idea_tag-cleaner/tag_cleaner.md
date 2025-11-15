# ## TagCleaner module

The following regex places all of the following tags in memoQ with nothing:

(?:\[(?:[1-9]|[12]\d|30)\}|\{(?:[1-9]|[12]\d|30)\])

So text like this:

Laat de tractor nooit draaien in een afgesloten ruimte, tenzij de uitlaat naar buiten wordt afgevoerd [7}lucht.{8]

 Becomes this:
 
  Laat de tractor nooit draaien in een afgesloten ruimte, tenzij de uitlaat naar buiten wordt afgevoerd lucht.
  
  If you also want to eat any stray spaces around them, use:

\s*(?:\[(?:[1-9]|[12]\d|30)\}|\{(?:[1-9]|[12]\d|30)\])\s*

However, use this second one with caution because you can end up with words or other things joined together! It is safest to use the first one and then check manually if you need delete any extra spaces. 

[1}
{2]
[3}
{4]
etc (All the way up to very high numbers,  I suppose never realistically higher than thirty or forty)
 
  
  
Example sentence: "Swinging draw bar is used for pulling trailed￼ ￼trailed implements￼ ￼implements."
 
  
  
  
  
  