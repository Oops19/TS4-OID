# Alpha Preview Release
You are welcome to test it. It is quite stable but some timings still fail.
Traveling will cause a bunch of exceptions, please ignore them.

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
For the base game there are a few interactions.
Some base game interactions may result in removed outfit parts for sims.

### Shower
* Sims will turn around in shower instead of watching the wall.

### Vanilla 'Pillow Fight ...'
* Sims will undress their shoes and might lose outfit parts.

### Using Toilet
* Configuration removed. Handled and hard coded in DD.

### Feeding Baby
* Configuration removed. Handled and hard coded in DD.

### Play Sabbac
* Losers undress am outfit item.


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
* `[Kritical]BlowjobArcade1d.package`
* `[Kritical]CeladonUrinal1a.package`
* `[Kritical]ExerciseBike1b.package`
* `[Kritical]FeedingMachine1d.package`
* `[Kritical]LetheUrinal1a.package`
* `[Kritical]MajesticHole1f.package`
* `[Kritical]MilkingMachine1d.package`
* `[Kritical]PracticalSexArcade1j.package`
* `[Kritical]SensoryDeprivationChamber1a.package`
* `[Kritical]StyxUrinal1h.package`
* `[Kritical]TanningRack1a.package`
* `[Kritical]Thighmaster1a.package`
* `[Kritical]WorkoutMachineFreya1a.package`

This mod has been tested with the versions mentioned above.

The mod injects into the interactions to make them compatible with DD.


#### Issues
Commands may be executed shortly after an interaction starts and shortly before an interaction stops.
It's not perfect but hopefully good enough for TS4.
Some of the issues mentioned below may have been fixed so far.

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

## Customized Custom User Customization
You read the title successfully, so you may start to adjust random vanilla and/or mod interactions as you like.

#### Gather the interaction IDs
There are two options to get interaction IDs

##### Log interaction IDs
* Press Shift+Ctrl+C to open the debug console
* Enter `o19.oid.log_sim` to log the queued interactions of the active sim.
* Optionally, this is usually Not Needed, log the pre-run interactions with  `o19.oid.log_sim_pre_run`
* Run the command again to disable logging.

##### Gather the interaction IDs with S4CL
* Pause the game and click on object X and select the interaction. It will be queued in the interaction Q.
* Sim+Shift-click > S4CL > Show running interactions to ge the IDs/Names or running and/or queued interactions.
* Un-pause the game and wait until the sim is using the object.
* Shift-click > S4CL > Show running interactions to ge the IDs/Names or running and/or queued interactions.
* The 'interact' and the 'interacting' interactions may be two different ones.

##### Create Configuration File
* Use your name and replace `author` (unless everyone calls you 'author' already).
* Replace `interaction_description` with the intention of the modification.
* Replace the `tunings` value with the interaction name(s), e.g. `celebrity_Self_PoseforPicture`.
  * Optionally use S4S to search for similar interactions (with `interaction/celebrity_Self_`). There you'll find 3.
  * You could add these 3 interactions or `celebrity_Self_` - in case a new self interaction is added your customization will modify it without any update.
* Then we need an idea what to do. For now add `g_debug_alert(celeb)` and `g_info_alert(celeb)`.
* Save the file to `mod_data/on_interaction_do/cfg/` and hope you didn't break it.
  * Optionally validate the contents with https://codebeautify.org/python-formatter-beautifier
* Reload the data with `o19.oid.patch` or `o19.oid.patch_verbose` which logs more data while patching to TS4-Library_*_Messages.txt.
  * In case the file is broken validate it with https://codebeautify.org/python-formatter-beautifier
```json
{
    "author_interaction_description*": {  # TODO adjust
        "filter": {
            "tunings": ["TuningName_as_logged_by_S4CL", "TuningName_2_as_logged_by_S4CL", ],
        },
        "actions": {
            "start_of_animation*": {  # TODO adjust
				"parameters": ["g_debug_alert(111)", ],
                "timing": "at_beginning",
            },
            "end_of_animation*": {  # TODO adjust
                "parameters": ["g_info_alert(111)", ],
			},
        },
    },
}
```
* The keywords 'filter, tunings, actions, parameters, timing' must not be modified.
* Adjust the keywords ending with '*' to match your needs.
* Unlike `json` comments are supported and `,}` and/or `,]` work fine. This allows to add new lines / statements without appending,` to the line above.

* Run again the interaction - with a random sim - and enjoy the modified configuration.

##### debug.txt
In case too much is going and/or patched save the file as 'debug.txt' or 'author_debug.txt'.
In case one or more debug files exist it/they will be read and applied - the standard configuration is ignored.
To 'undo' all applied modifications restart the game and then test the debug settings.
Reload them with `o19.oid.patch`.

After testing copy the contents to a regular configuration file and delete the/all debug file(s).
With `o19.oid.patch` the files will be read and applied again, without restarting the game.

### Supported 'actions'
To modify how interactions start or end some commands are available.
Some additional settings are also available and shown below.
```json
{
    "author_interaction_description*": {
        'actions': {
            "start_of_animation*": {
                'drop_all_basic_extras': True,  # drop everything with <I><L n="basic_extras">[...]</L>
                'drop_basic_extras': [  # or drop individual elements within <I><L n="basic_extras">, supported are
                    'TunableBroadcasterRequestWrapper.BroadcasterRequest',
                    'TunableBuffElementWrapper.factory',
                    'TunableChangeOutfitElementWrapper.ChangeOutfitElement',
                    'TunableDoCommandWrapper.DoCommand',
                    'TunableLootElementWrapper.LootElement',
                    'TunableNotificationElementWrapper.NotificationElement',
                    'TunablePlayVisualEffectElementWrapper.PlayVisualEffectElement',
                    'TunablePregnancyElementWrapper.PregnancyElement',
                    'TunableStateChangeWrapper._factory',
                    'TunableTunableAudioStingWrapper.TunableAudioSting',
                ],
                'timing': 'at_beginning',  # or 'at_end' or 'on_xevt'
                'offset_time': 5,  # optionally, only valid for 'at_beginning'
                'xevt_id': 123,  # only valid for 'on_xevt'
                'include_target_sim': True,  # can be set to False
                'include_target_object': False,  # setting this to True sets  include_target_sim=False
                'parameters': ['...', ],
            },
        },
    },
}
```
For `parameters` these commands are available:
* `g_repeat(tunings_ref, 900, 30)` - Repeat the following commands for max. 900 seconds, every 30 seconds, while the sim is running one of the interactions in "filter.tunings".
* `g_random(10)` - 10% change to continue with the next command (range 1-99)
* `g_rotate_abs(340)` - Rotate the sim slowly to -20° (range 1-359)
* `g_rotate_rnd(180, 10)` - Rotate the sim slowly to a position between -170° - 190° (180° ± 10°) - range(1-359, 1-179)
* `g_rotate_end` - Stop the rotation before it completed.
* `g_opacity(0.8, 10)` - Fade the sim to 80%% opacity within 10 seconds. range(0.0-1.0, 0-30)
* `g_debug_info(Message)` - Show a blue popup for debug purposes.
* `g_debug_alert(Message)` - Show an orange popup for debug purposes.
* `bg_impregnate` - Impregnate the target sim (target sim must be set !)
* `s_undo_outfit` - Undo outfit changes created by one of the following parameters at the end of the interaction.
* `s_undo_outfit(200)` - In case the interaction is still running after 200s undo the outfit change. (range 1-999)
* `s_undo_outfit(200, 30)` - As above, but wait 30 seconds before undo.
* `s_undress_cas_parts(5, 6, 7)` - Remove CAS / body types from the sim. 5=FULL_BODY, 6=TOP, 7=BOTTOM (range 1-200, not every part is supported)
* `s_equip_cas_parts` - Equip CAS / body types
* `s_undress_all`, `s_undress_full`, `s_undress_top`, `s_undress_bottom`, `s_undress_shoes` - Remove CAS parts
* `s_equip_all`, `s_equip_full`, `s_equip_top`, `s_equip_bottom` - Add CAS parts
* `s_undress_next` - Remove one CAS part. The types and order is pre-defined. Might be called in a loop.
* `s_undress_next(7, 6)` - Remove one CAS part in the specified order. Might be called in a loop.

### Supported 'filters'
Usually it is fine just to specify `tunings`.

The default tuning manager is 'INTERACTION', this can be modified if needed.
The configuration files of this mod always call their own cheat command 'o19.oid.do_command' (default) which can also be modified.
One call can call cheat commands of random mods while the supplied command parameters will usually not match.
A list of buffs and traits can also be generated to be used by 'commands'.
The 'tunings' can be specified as strings starting and or ending with '*' for wildcards.
Use wildcards with care, `*a*` matches almost all tunings and may cause out of memory issues and take less than eternity to complete.

```json
{
    "author_interaction_description*": {
      "filter": {
        'traits': ['...', ],
        'buffs': ['...', ],
        'manager': 'INTERACTION',  # or 'SNIPPET' to modify a snippet tuning
        'tunings': ['...', ],
        'command': 'o19.oid.do_command',
      }, ...
```

### Supported 'commands'
Within 'commands' a few special commands are supported. It contains a list of 1-n commands.
```json
{
    "author_interaction_description*": {
        "filter": {
            'traits': ['...' ],
            'buffs': ['...' ],
            ...
        },
        "commands": [
            ...
        ]
    }
}
```
* `remove_privacy` Remove privacy checks (`<I>[<V n="privacy" ...</V>]`)
* `no_gender_check` Remove gender checks (`<I><L n="test_globals">[<E n="gender">...</E>]`)
* `drop_tg_TEST` with TEST=BuffTest, CareerGigTest, CommodityAdvertisedTest, SimInfoTest, SkillRangeTest, TraitTest
  * `drop_tg_BuffTest` removes all Buff tests from 'test_globals'. This might cause issues for further tests.
* `ACTION_LIST_TYPE` Eight commands with ACTION=add or remove, LIST=whitelist or blacklist and TYPE=buffs or traits from test_globals
  * `add_whitelist_buffs` `add_blacklist_buffs` `add_whitelist_traits` `add_blacklist_traits` 
  * `remove_whitelist_buffs` `remove_whitelist_buffs` `remove_blacklist_traits` `remove_blacklist_traits`
  * All six other variations work like these two samples:
  * `add_whitelist_traits` Add the 'filter.traits' to the allow list
  * `remove_blacklist_buffs` Remove the 'filter.buffs' from the deny list. Set 'filter.buffs' to 'True' to remove everything.
  * To add buffs and two remove other buffs two `author_interaction_description` sections are needed as only one `buffs` and `traits` section exist.
* `ACTION_LIST_TYPE_test` Eight commands with ACTION=add or remove, LIST=whitelist or blacklist and TYPE=buffs or traits from `n="testSet..."` tunings ().
  * `add_whitelist_buffs_test`, ...  see above for details.

---

# 📝 Addendum

## 🔄 Game compatibility
This mod has been tested with `The Sims 4` 1.120.117, S4CL 3.17, TS4Lib 0.3.42.
It is expected to remain compatible with future releases of TS4, S4CL, and TS4Lib.

## 📦 Dependencies
Download the ZIP file - not the source code.
Required components:
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not already installed, download and install TS4 and the listed mods. All are available for free.

## 📥 Installation
* Locate the localized `The Sims 4` folder (it contains the `Mods` folder).
* Extract the ZIP file directly into this folder.

This will create:
* `Mods/_o19_/$mod_name.ts4script`
* `Mods/_o19_/$mod_name.package`
* `mod_data/$mod_name/*`
* `mod_documentation/$mod_name/*` (optional)
* `mod_sources/$mod_name/*` (optional)

Additional notes:
* CAS and Build/Buy UGC without scripts will create `Mods/o19/$mod_name.package`.
* A log file `mod_logs/$mod_name.txt` will be created once data is logged.
* You may safely delete `mod_documentation/` and `mod_sources/` folders if not needed.

### 📂 Manual Installation
If you prefer not to extract directly into `The Sims 4`, you can extract to a temporary location and copy files manually:
* Copy `mod_data/` contents to `The Sims 4/mod_data/` (usually required).
* `mod_documentation/` is for reference only — not required.
* `mod_sources/` is not needed to run the mod.
* `.ts4script` files can be placed in a folder inside `Mods/`, but storing them in `_o19_` is recommended for clarity.
* `.package` files can be placed in a anywhere inside `Mods/`.

## 🛠️ Troubleshooting
If installed correctly, no troubleshooting should be necessary.
For manual installs, verify the following:
* Does your localized `The Sims 4` folder exist? (e.g. localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...)
  * Does it contain a `Mods/` folder?
    * Does Mods/_o19_/ contain:
      * `ts4lib.ts4script` and `ts4lib.package`?
      * `{mod_name}.ts4script` and/or `{mod_name}.package`
* Does `mod_data/` contain `{mod_name}/` with files?
* Does `mod_logs/` contain:
  * `Sims4CommunityLib_*_Messages.txt`?
  * `TS4-Library_*_Messages.txt`?
  * `{mod_name}_*_Messages.txt`?
* Are there any `last_exception.txt` or `last_exception*.txt` files in `The Sims 4`?


* When installed properly this is not necessary at all.
For manual installations check these things and make sure each question can be answered with 'yes'.
* Does 'The Sims 4' (localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...) exist?
  * Does `The Sims 4` contain the folder `Mods`?
    * Does `Mods` contain the folder `_o19_`? 
      * Does `_19_` contain `ts4lib.ts4script` and `ts4lib.package` files?
      * Does `_19_` contain `{mod_name}.ts4script` and/or `{mod_name}.package` files?
  * Does `The Sims 4` contain the folder `mod_data`?
    * Does `mod_data` contain the folder `{mod_name}`?
      * Does `{mod_name}` contain files or folders?
  * Does `The Sims 4` contain the `mod_logs` ?
    * Does `mod_logs` contain the file `Sims4CommunityLib_*_Messages.txt`?
    * Does `mod_logs` contain the file `TS4-Library_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
    * Does `mod_logs` contain the file `{mod_name}_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
  * Doesn't `The Sims 4` contain the file(s) `last_exception.txt`  and/or `last_exception*.txt` ?
* Share the `The Sims 4/mod_logs/Sims4CommunityLib_*_Messages.txt` and `The Sims 4/mod_logs/{mod_name}_*_Messages.txt`  file.

If issues persist, share:
`mod_logs/Sims4CommunityLib_*_Messages.txt`
`mod_logs/{mod_name}_*_Messages.txt`

## 🕵️ Usage Tracking / Privacy
This mod does not send any data to external servers.
The code is open source, unobfuscated, and fully reviewable.

Note: Some log entries (especially warnings or errors) may include your local username if file paths are involved.
Share such logs with care.

## 🔗 External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## ⚖️ Copyright and License
* © 2020-2025 [Oops19](https://github.com/Oops19)
* `.package` files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* All other content (unless otherwise noted): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 

You may use and adapt this mod and its code — even without owning The Sims 4.
Have fun extending or integrating it into your own mods!

Oops19 / o19 is not affiliated with or endorsed by Electronic Arts or its licensors.
Game content and materials © Electronic Arts Inc. and its licensors.
All trademarks are the property of their respective owners.

## 🧾 Terms of Service
* Do not place this mod behind a paywall.
* Avoid creating mods that break with every TS4 update.
* For simple tuning mods, consider using:
  * [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
  * [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To verify custom tuning structures, use:
  * [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).

## 🗑️ Removing the Mod
Installing this mod creates files in several directories. To fully remove it, delete:
* `The Sims 4/Mods/_o19_/$mod_name.*`
* `The Sims 4/mod_data/_o19_/$mod_name/`
* `The Sims 4/mod_documentation/_o19_/$mod_name/`
* `The Sims 4/mod_sources/_o19_/$mod_name/`

To remove all of my mods, delete the following folders:
* `The Sims 4/Mods/_o19_/`
* `The Sims 4/mod_data/_o19_/`
* `The Sims 4/mod_documentation/_o19_/`
* `The Sims 4/mod_sources/_o19_/`
