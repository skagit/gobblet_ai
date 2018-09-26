# Motivation

I was introduced to the game - Gobblet - at a friend's house a while back. However, he and I cannot get together to play as often as we would like, and I got the distinct impression that neither my wife or his enjoy the game as much as we do. In my experience, the combinatino of board games and bored wives provides the perfect opportunity to do a little software engineering with an AI component.

# The Game of Gobblet

Gobblet is a two-player game that takes place on a small, 4 X 4 board of squares. To win, one player must get 4 pieces of their color in a row (including the diagonals). Each turn, a player can place one of their pieces into any empty square, which so far makes it essentially tic-tac-toe on an expanded board. However, Gobblet has a number of simple additions that make it so much more.

The first such addition, is that instead of moving a piece from your hand onto the board, a player can move a piece already on the board to any open position. The board is dynamic.

The second addition, is that pieces come in four sizes - let's call them large, medium, small, and tiny - and with three pieces in each size, there are 12 pieces all together. Like nested Russian dolls, the larger pieces are made to stack on top of the smaller ones.

This size component comes into play as follows. Any piece already on the board, can be moved into an empty space, or on top of any other piece on the board smaller than it. To clarify, it is perfectly legal to 'gobble' up one's own pieces in this manner, and the size difference need not be simply the next size lower.

Normally, a piece played from off the board cannot gobble, and so must be placed on an empty square. However, if an opponent has three pieces already lined up in a row, a player may gobble any one of those three directly with the piece taken from the hand.

Finally, the game begins with each player having their pieces in three stacks, and one must play the larger pieces in a stack before playing the smaller ones. For example, the first move must be one of the three large pieces on top of the stacks. The next move for the same player could either be to relocate the large piece just played, or to play one of the two large pieces or now exposed medium piece from their hand. There are a few rare minutiae such as when a draw occurs and what happens if you pick up a piece you cannot play elsewhere, but the above description provides more than enough to enjoy the game, and interested parties can find [a copy of the rules](https://www.boardspace.net/gobblet/english/gobblet_rules.pdf) online for free.
