Change data to follow real world example:
- Parisian appartement prices in function of the surface

In the 3D plot of cost, the derivate is given at the same time as multiplot
It might be better to break it in two separate graph so the information is more digest


Plan du cours:

- 1 Human and manual machine learning
  -> The data has a linear correlation
  -> There exist a function great for that kind of relationship: ax + b
  -> We can interact visually with our manual LR
- 2 Cost function
  -> Let's stop eye balling the data, and let's start to compute the cost
  -> We can choose a good fit
- 3 Let's automate
  - 1 An inefficient optimization process
    -> We can sample random points and hope to get lucky
  - 2 Getting rid of the randomness:
    -> What if we knew how to change parameters for a given point?
	-> Finite differentiation
	-> Complexity 
  - 3 Let's get analytical
    -> We can use gradient descent to find the minimum of the cost function
	-> computational graph
