# tAkumI 

## What is it?
tAkumI is a project that will use the Reinforement Learning methodology known as NEAT (NeuroEvolution of Augmenting Topologies) to teach a neural network to drive a 2d car on a multitude of different tracks. This will be done in Python. I think AI is cool, and I think most people who drive are bad at it, so an AI that can drive is cool and better than what we have now.

## Notes
- There will be 5 sensors that the AI will take in so that it can be aware of and look out for the borders of the track. Those will be to the right, to the left, diagnolly to the left, diagnolly to the right, and straight ahead.
- There are 4 output neurons that represent the 4 actions that the AI can take. Those are turn left, turn right, speed up and slow down.
- There are 2 main parts to the project. The python file, and the config-feedforward file.
    - The python file will contain the code needed to run the tracks, car, the neural network, and everything else.
    - The config-feedforward file will allow the adjusting of various parameters for the neural network.