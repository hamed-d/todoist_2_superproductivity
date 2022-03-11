# Todoist to Super Productivity Integration
This is a simple python script for integrating Todoist and Super Productivity (SP).

## :question: How it works
By running the script your tasks in Todoist from the current date will be added to SP. There is also an option to deal with subtasks where you can either add only the parent task or add only subtasks.

## :question: How to use it

### Setting up syncing in Super Productivity
First you need to set up syncing in SP. Open SP and go to settings. At the bottom of the page open up "Sync" and check the "Enable Syncing" option. Set the interval on something more than 1 minute and put "Sync Provider" on "LocalFile". Set "Sync file path" to anything you'd like but make sure the name of the file is vault. As an example, "S:/SPVault/vault". Click on Save and you are done with this section.

### Integrating Todoist with SP
1. Login to Todoist using your browser and click on your profile on the top right and go to integrations. On the bottom of the opened page, in the API Token section, copy the token to your clipboard.
2. After making sure you have set up syncing in Super Productivity. Open Super Productivity and click on the refresh button on the top-right corner.
3. Now you need to run the script. The script has three arguments. The path to vault (from the syncing section above), API token for Todoist and finally, an option to determine whether you want to add subtasks or the parent task only. You need python 3.x installed. An example of the command is as follows.
    ```
    python todoist_syncer.py --path S:/SPVault/ --token <your token goes here> --subtasks True
    ```
   Running this script will create a new file in the same path that should be imported to SP.
4. Now, go to SP>Setting>Import/Export and select "IMPORT FROM FILE" and select the new file from the path (according to the example it would be S:/SPVault/synced_vault.json) and that's it. You should now see the tasks from Todoist in SP.