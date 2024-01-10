# ZTF-Interference
The ZTF-Interference tool implements interference modeling from n numbers of non-necessarily point sources. The non-pointedness of the source is modeled as several very close point sources (sub-sourcese of source).

The simulated system has variable parameters:
- Time;
- The number of sources;
- The number of sub-sources to emulate non-point source;
- The distance between the sources;
- The distance between the sources and the screen;
- The size of screen;
- The amplitude of the source waves;
- The length of the source waves;
- The speed of the source waves;
- The initial phase of the source waves.

The addition of waves is realized by the method of vector diagrams.

ZTF-Interference tool allows to add custom types of sources by creating it's class with "amplitude" and "phase" fields.

![scheme](/img1.png)

An example of the interference simulation for two point sources (time = 200 s, the distance between the sources = 0.4 m, the distance between the sources and the screen = 4 m, the size of screen = 50 m, the amplitude of the source waves = 1, the length of the source waves = 0.017 m, the speed of the source waves = 340 m/s, initial phase of the source waves = 0):

![example](/img2.png)
