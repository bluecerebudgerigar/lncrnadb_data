#!/usr/bin/env python 

from cmsexporter_pythonclass import *


sequence_worker =  SequenceWorker(6000)
sequence_worker.read_file("data/Annotation_V3.tsv.txt", "annotation")
sequence_worker.read_file("data/sequences.tsv", "sequences")
sequence_worker.add_names("data/key_value.txt")

character_worker = CharacterWorker(2000)
character_worker.read_csv("data/character_annotation.csv", "characteristics")
character_worker.files["annotation"] = sequence_worker.files["annotation"]

literature_worker = LiteratureWorker(4000)
literature_worker.files["annotation"] = sequence_worker.files["annotation"]
literature_worker.read_csv("data/literature_annotation.csv","literature")

species_worker = SpeciesWorker(3000)
species_worker.files["annotation"] = sequence_worker.files["annotation"]
species_worker.read_csv("data/species_annotation.csv", "species")

assoc_worker = AssocWorker(5000)
assoc_worker.files["annotation"] = sequence_worker.files["annotation"]
assoc_worker.read_csv("data/associatedcomp_annotation.csv", "associatedcomp")

alias_worker = AliasWorker(1000)
alias_worker.files["annotation"] = sequence_worker.files["annotation"]
alias_worker.read_csv("data/nomenclature_annotation.csv","nomenclature")

character_worker.match(content='characteristics')
sequence_worker.match()
sequence_worker.search_ncbi()
sequence_worker.fixup()
print sequence_worker.fixed

literature_worker.match(content='literature')
species_worker.match(content='species')  
assoc_worker.match(content='associatedcomp')
alias_worker.match(content='nomenclature')

species_worker.fixup()
literature_worker.fixup()
character_worker.fixup()
assoc_worker.fixup()
sequence_worker.fixup()
print sequence_worker.files['sequences']

alias_worker.fixup()


literature_worker.fixed
character_worker.fixed

assoc_worker.fixed
sequence_worker.fixed
alias_worker.fixed

species_worker.write_csv("output/species.csv")
literature_worker.write_csv("output/literature.csv")
character_worker.write_csv("output/character.csv")
assoc_worker.write_csv("output/assoc.csv")
sequence_worker.write_csv("output/sequence.csv")
alias_worker.write_csv("output/alias.csv")

master_controller=MasterController()

master_controller.additems(literature_worker,character_worker,species_worker,assoc_worker,sequence_worker,alias_worker)

master_controller.check_consenses()
master_controller.add_identifer("data/key_value.txt")
master_controller.build_cmsplugin()
master_controller.write_csv()




sequence_worker =  SequenceWorker(60000)
sequence_worker.read_file("data/Annotation_V3.tsv.txt", "annotation")
sequence_worker.read_file("data/sequences.tsv", "sequences")
sequence_worker.add_names("data/key_value.txt")

character_worker = CharacterWorker(20000)
character_worker.read_csv("data/character_annotation.csv", "characteristics")
character_worker.files["annotation"] = sequence_worker.files["annotation"]

literature_worker = LiteratureWorker(40000)
literature_worker.files["annotation"] = sequence_worker.files["annotation"]
literature_worker.read_csv("data/literature_annotation.csv","literature")

species_worker = SpeciesWorker(30000)
species_worker.files["annotation"] = sequence_worker.files["annotation"]
species_worker.read_csv("data/species_annotation.csv", "species")

assoc_worker = AssocWorker(50000)
assoc_worker.files["annotation"] = sequence_worker.files["annotation"]
assoc_worker.read_csv("data/associatedcomp_annotation.csv", "associatedcomp")

alias_worker = AliasWorker(10000)
alias_worker.files["annotation"] = sequence_worker.files["annotation"]
alias_worker.read_csv("data/nomenclature_annotation.csv","nomenclature")

character_worker.match(content='characteristics')
sequence_worker.match()
sequence_worker.search_ncbi()
literature_worker.match(content='literature')
species_worker.match(content='species')  
assoc_worker.match(content='associatedcomp')
alias_worker.match(content='nomenclature')

species_worker.fixup()
literature_worker.fixup()
character_worker.fixup()
assoc_worker.fixup()
sequence_worker.fixup()
alias_worker.fixup()


literature_worker.fixed
character_worker.fixed

assoc_worker.fixed
sequence_worker.fixed
alias_worker.fixed

species_worker.write_csv("output/species.csv")
literature_worker.write_csv("output/literature.csv")
character_worker.write_csv("output/character.csv")
assoc_worker.write_csv("output/assoc.csv")
sequence_worker.write_csv("output/sequence.csv")
alias_worker.write_csv("output/alias.csv")


master_controller=MasterController()
master_controller.additems(literature_worker,character_worker, species_worker, assoc_worker,sequence_worker,alias_worker)
master_controller.check_consenses()

master_controller.add_identifer("data/key_value.txt")
master_controller.build_cmsplugin_publisher()
master_controller.write_csv()

#character_worker.print_content()
#sequence_worker.print_content()6666666666666666666666666666666666666666666
#literature_worker.print_content()
#species_worker.print_content()  
#assoc_worker.print_content()
##print sequence_worker.seq_entries
##print sequence_worker

