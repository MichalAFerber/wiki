# ModMan

---

*Mod Manager for the Farming Simulator 2019 game*

Windows application is written in C# that modifies XML files. Created, changed, upgraded, and maintained since April 23, 2020

**Created April 23, 2020**

[![GitHub Release](https://img.shields.io/github/v/release/MichalAFerber/ModMan)](https://github.com/MichalAFerber/ModMan/releases/) [![GitHub Release Date](https://img.shields.io/github/release-date/MichalAFerber/ModMan)](https://github.com/MichalAFerber/ModMan/releases/) [![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/MichalAFerber)](https://x.com/MichalAFerber)

*==This README was last updated on May 02, 2022==*  

- [Installation](#installation)
- [Setting It Up](#setting-it-up)
- [Advanced Settings](#advanced-settings)

Mod Manager for Farming Simulator 2019. FS19 game XML file and mod manager. Easy to use, simple interface, and only one file.

Latest Build: [Version 2020.04.23.0001](https://github.com/MichalAFerber/ModMan/releases/download/2020.04.23.001/ModMan_v2020_04_23_0001.zip) | [GitHub](https://github.com/MichalAFerber/ModMan)

![[ModManAbout.png]]

## Installation

Unzip the downloaded file and place the file wherever you desire, I placed mine in the folder `C:\Program Files (x86)\ModMan`. I also created a shortcut to it and placed it on my desktop. The first time you run the program you may get a blue box as shown below. Click the `More info` link.

![[WindowsProtected1.png]]

Then click the `Run anyway` button. You should only encounter this the first time you run the program.

![[WindowsProtected2.png]]

[Back to top](#modman)

## Setting It Up

Now that the program is up and working. You need to define the folders before the program will work properly.

**Application Folder**

If you are running FS19 through Steam then the default installation path is `C:\Program Files (x86)\Steam\steamapps\common\Farming Simulator 19`. Select this path or wherever you installed FS19. If you don’t know where you can right-click on the FS19 launch icon and select properties. On that screen, the START IN folder is what you are looking for.

![[FileProperties.png]]

**Game Settings Folder**  

The settings folder is the location of the FS19 game.xml and gamesettings.xml.

```
C:\Users\YourNameHere\Documents\My Games\FarmingSimulator2019\
```

**Mod Folder Root**  

This is the root of the folder that contains all of your different mod folders. If you have never separated your mods before now, then this folder will have to be created. For me, I put my separate mod folders in the default FS19 mod folder location.

```
C:\Users\YourNameHere\Documents\My Games\FarmingSimulator2019\mods\
```

![[ModMan1.png]]

[Back to top](#modman)

## Advanced Settings

**Developer Mode**  

This enables the developer console in the game will allow you to type commands. A great article on what you can do with developer mode is [here](https://www.yekbot.com/farming-simulator-19-console-commands-developer-console/).

**Audio**   

This turns the audio on or off and sets the volume level percentage.

```
Examples:
1.0000 = 100%
0.7000 = 70%
```

**Logging**  

This turns the logging for the game on or off and allows you to change the filename the log will use. The default for the game is logging enabled and the log filename log.txt.

![[ModManShowAdvancedMenuOption.png]]

![[ModManSelectedModFolder.png]]

[Back to top](#modman)
