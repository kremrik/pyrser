# Pyrser
A simple tool to visualize function calls in Python modules

### Where are we at?
So far, we have the basic groundwork completed:
- Ability to serialize a .py file into a custom graph
- Ability to visualize a .py file's calls with graphviz

### What's next?
* [x] Functionality to pass pyrser a directory
* [ ] Add functions in jupyter notebook to ``Pyrser.py``
* [ ] Ability to determine where a function came from, from with a module (in the event names are the same and the module is aliased like mod.fnc())
* [ ] Simple webserver to server the graphviz as html
* [ ] In the future, a D3js representation of the graphviz output to allow users to click on functions and see the actual source code
* [ ] More sophisticated blacklisting rules to eliminate hidden dirs/files (ex, ``.git``)
