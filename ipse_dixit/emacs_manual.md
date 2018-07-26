<< [go back](https://apiraino.github.io)

# How the EMACS manual explains what a local variable is


> let is used to attach or bind a symbol to a value in such a way that the Lisp interpreter will not confuse the variable with a variable of the same name that is not part of the function.

> To understand why the let special form is necessary, consider the situation in which you own a home that you generally refer to as “the house”, as in the sentence, “The house needs painting.” If you are visiting a friend and your host refers to “the house”, he is likely to be referring to his house, not yours, that is, to a different house.

> If your friend is referring to his house and you think he is referring to your house, you may be in for some confusion. The same thing could happen in Lisp if a variable that is used inside of one function has the same name as a variable that is used inside of another function, and the two are not intended to refer to the same value. The let special form prevents this kind of confusion.

[link to the manual](https://www.gnu.org/software/emacs/manual/html_node/eintr/let.html)

<< [go back](https://apiraino.github.io)
