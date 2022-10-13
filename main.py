import json
from difflib import SequenceMatcher


def main():
    # load the data
    f_bukkit = open('../scraperRepository/bukkitResourcesData.json', 'r')
    bukkit = json.load(f_bukkit)
    f_bukkit.close()

    f_spigot = open('../scraperRepository/spigetResources.json', 'r')
    spigot = json.load(f_spigot)
    f_spigot.close()

    # array of bukkit plugins and its best spigot plugin match
    matches = []

    for bukkit_plugin in bukkit:
        # get the best match
        plugin_matches = []
        for i, spigot_plugin in enumerate(spigot):
            ratio_name = SequenceMatcher(None, bukkit_plugin["title"], spigot_plugin["name"]).ratio()
            ratio_desc = SequenceMatcher(None, bukkit_plugin["desc"], spigot_plugin["tag"]).ratio()
            # ratio_authors = 0
            # if "contributors" in spigot_plugin:
            #     ratio_authors = SequenceMatcher(None, ', '.join(bukkit_plugin["authors"]), spigot_plugin["contributors"]).ratio()
            ratio_source = 0
            if "source" in bukkit_plugin and "sourceCodeLink" in spigot_plugin:
                ratio_source = SequenceMatcher(None, bukkit_plugin["source"], spigot_plugin["sourceCodeLink"]).ratio()
            
            ratio = (ratio_name + ratio_desc + ratio_source**2)/3
            plugin_matches.append((i, ratio))

        # sort the matches
        plugin_matches.sort(key=lambda x: x[1], reverse=True)

        if "icon" in spigot[plugin_matches[0][0]]:
            del spigot[plugin_matches[0][0]]["icon"]
        matches.append((plugin_matches[0], bukkit_plugin, spigot[plugin_matches[0][0]]))
        print(matches[-1])
        print()

    # already matched plugins
    matched = []

    # sort the matches
    matches.sort(key=lambda x: x[0][1], reverse=True)

    # array of bukkit plugins and its best spigot plugin match
    final_matches = []
    for match in matches:
        if match[0][0] not in matched:
            final_matches.append(match)
            matched.append(match[0][0])
    
    # save the matches
    f_matches = open('../scraperRepository/matches.json', 'w')
    json.dump(final_matches, f_matches, indent=2)

if __name__ == "__main__":
    main()
