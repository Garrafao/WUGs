# Insert tutorial

## Steps
To insert tutorial, one should create a new docker compose file which specifically serves this purpose, have a look at the docker-compose_insert_tutorial file for reference. 

The only difference between the docker-compose.yml file and the docker-compose_insert_tutorial.yml file is the extra line below:
```
command: -t /durel_system/app/tutorials/encoded-it_fixed.csv /durel_system/app/tutorials/encoded-it_jud.csv "placeholder" "it"
```
This extra line makes sure the application will execute some extra functions that insert new tutorial into the postgres database when launching.

You can refer to the Server.java file and the Argprs.java file in the repository for relevant source code.

## Tutorial Format
One should provide two csv file. 

The first file provide uses. Please check the [sample file](https://github.com/Garrafao/WUGs/blob/main/durel_system/tutorials/tutorial_sentences/english.csv) and strictly follows this format. Note the value under indexes column corresponds to word position. For example, the first word in the sentence has the index 0.

The second file provide judgments. Please check  [sample file](https://github.com/Garrafao/WUGs/blob/main/durel_system/tutorials/tutorial_gold_annotations/english.csv) and strictly follows this format. The identifier in the identifiers1 and identifiers2	column should correspond to the identifier provided in the first file.

