# Alpha Preview Release
You are welcome to test it. It is quite stable but some timings still fail.
Travelling may cause a bunch of exceptions, please ignore them.

#  On Interaction Do

This is a script mod to run various commands whenever a sim is executing an action.

It supports many base game interactions, and support for some mods.
It uses the appearance modifiers provided by Devious Desires / Core and it is not compatible with 'wicked' script mods.

This mod currently requires Devious Desires / Core to be able to use appearance modifiers.

## Code and/or included Content
This mod only references object and/or tuning names of interactions etc.
This mod does not
* add new interactions
* add new items
* include or override UGC created by other mod creators


## Base Game
For the base game there are a few interactions.ase game interactions wi
Some base game interactions may result in removed outfit parts for sims.

### Vanilla Toilet
* Sims will undress when they use the toilet.

### ?
There is more, I'm sure there is


## 3rd party mods and build items

### HIU
HIU by Sacrificial is supported, while it is not required.
If HIU is installed make sure to remove these script mods:
* `wicked*.ts4script`

The actors support the basic un-/equip commands as used by HIU.

### Build Items
Some devices by Kritical are supported, none of them is required.
Just make sure to remove these script mods:
* `[Kritical]StyxUrinal1.ts4script`  # and/or similar versions
* `[Kritical]PracticalSexArcade1.ts4script`  # and/or similar versions

The following devices are supported:
* `[Kritical]StyxUrinal.package` - Version 1h
* `[Kritical]PracticalSexArcade.package` - Version 1i
* `[Kritical]BlowjobArcade.package` - Version 1c
* `[Kritical]LetheUrinal.package` - Version 1a
* `[Kritical]MilkingMachine1.package`
* ...
* `[Kritical]ExerciseBike.package` - Version 1b
* `[Kritical]SensoryDeprivationChamber.package` - Version 1a
* `[Kritical]Thighmaster.package` - Version 1
* 
* `[Kritical]FeedingMachine.package` - Version 1d
* `[Kritical]MilkingMachine.package` - Version 1c

Not supported / No interaction:
* `[Kritical]CeladonUrinal.package` - Version 1a

This mod has been tested with the versions mentioned above.

To lower the pee time for the 'LetheUrinal' install PatchXML.

The mod injects into the interactions to make them compatible with DD.


#### Issues
Commands may be executed shortly after an interaction starts and shortly before an interaction stops. It's not perfect but hopefully good enough for TS4.

##### Sex and BJ Arcade
* Customers will undress the lower body and dress up afterwards properly, the initial state (nude, underwear, outfit) will be restored.
* The gender check has been removed, customers without a penis will use a strap-on.
* Customers with a penis will get a boner during animation. Flaccid afterwards, also the cum level will be reduced.

##### Styx Urinal
* Customers will undress the lower body and dress up afterwards properly, the initial state (nude, underwear, outfit) will be restored.
* Not modified: The game may rotate the sim or the effect 180° and it may look odd. 

##### Milking Machine
* Sims with a Basic, Upgraded or Reward trait can use it.
* Sims will undress the upper body and dress up afterwards properly, the initial state (nude, underwear, outfit) will be restored.
* The milk level will be reduced after milking. This is not related to the amount of milk available in the machine.
* Sims will no longer fade-out and fade-in as it didn't work reliable for me.
* Pregnant sims can milk themselves.

### Customization
#### Gather the interaction IDs with S4CL
* Pause the game and click on object X and select the interaction. It will be queued in the interaction Q.
* Sim+Shift-click > S4CL > Show running interactions to ge the IDs/Names or running and/or queued interactions.
* Un-pause the game and wait until the sim is using the object.
* Shift-click > S4CL > Show running interactions to ge the IDs/Names or running and/or queued interactions.
* The 'interact' and the 'interacting' interactions may be two different ones.

##### Sample
With the two Names and/od IDs create your own customization.
```json
{
    "author_interaction_description*": {
        "filter": {
            "tunings": ["TuningName_as_logged_by_S4CL", "TuningName_2_as_logged_by_S4CL", ],
        },
        "actions": {
            "start_of_animation*": {
				"parameters": ["g_debug_alert(111)", ],
                "timing": "at_beginning",
            },
            "end_of_animation*": {
                "parameters": ["g_info_alert(111)", ],
			},
        },
    },
}
```
The keywords 'filter, tunings, actions, parameters, timing' must not be modified.
Adjust the keywords ending with '*' to match your needs.

# Addendum

## Game compatibility
This mod has been tested with `The Sims 4` 1.110.311, S4CL 3.9, TS4Lib 0.3.28 (2024-11-14).
It is expected to be compatible with many upcoming releases of TS4, S4CL and TS4Lib.

## Dependencies
Download the ZIP file, not the sources.
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not installed download and install TS4 and these mods.
All are available for free.

## Installation
* Locate the localized `The Sims 4` folder which contains the `Mods` folder.
* Extract the ZIP file into this `The Sims 4` folder.
* It will create the directories/files `Mods/_o19_/$mod_name.ts4script`, `Mods/_o19_/$mod_name.package`, `mod_data/$mod_name/*` and/or `mod_documentation/$mod_name/*`
* `mod_logs/$mod_name.txt` will be created as soon as data is logged.

### Manual Installation
If you don't want to extract the ZIP file into `The Sims 4` folder you might want to read this. 
* The files in `ZIP-File/mod_data` are usually required and should be extracted to `The Sims 4/mod_data`.
* The files in `ZIP-File/mod_documentation` are for you to read it. They are not needed to use this mod.
* The `Mods/_o19_/*.ts4script` files can be stored in a random folder within `Mods` or directly in `Mods`. I highly recommend to store it in `_o19_` so you know who created it.

## Usage Tracking / Privacy
This mod does not send any data to tracking servers. The code is open source, not obfuscated, and can be reviewed.

Some log entries in the log file ('mod_logs' folder) may contain the local username, especially if files are not found (WARN, ERROR).

## External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## Copyright and License
* © 2024 [Oops19](https://github.com/Oops19)
* License for '.package' files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* License for other media unless specified differently: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless the Electronic Arts TOS for UGC overrides it.
This allows you to use this mod and re-use the code even if you don't own The Sims 4.
Have fun extending this mod and/or integrating it with your mods.

Oops19 / o19 is not endorsed by or affiliated with Electronic Arts or its licensors.
Game content and materials copyright Electronic Arts Inc. and its licensors. 
Trademarks are the property of their respective owners.

### TOS
* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.
* For simple tuning modifications use [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
* or [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To check the XML structure of custom tunings use [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).
