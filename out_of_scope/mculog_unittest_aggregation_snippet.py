

parsedLogLineSpec1 = [pt.parseLineID,"DuckBand", ]

nicknames = [[pt.parseLineID, "Young Dux Nicknames"], ["Dewey", "rabbit"], ["Luey", 2],
                 ["Huey", "Scrooge MacDuck"], ["Phred", "Fearless Fly"]]

pllBandMembers = [[pt.parseLineID, "band members"],["vocalist", "Huey"],["bass player", "Luey"], ["drummer","Dewey"],
               ["lead guitar","Phred"]]
pllInstruments = [[pt.parseLineID, "accent instruments"],["MoneyBin Blues","Daffy's Noggin"],
               ["Weasel! goes the Pop!","Marvin's Helmet Drum"], ["Soylent Running","Dessert Spoons"],
               [ "Warner Bros Rabbit","Mouth Harp"]]
pllMusicPieces = [[pt.parseLineID, "music pieces"],["Set Opener","Warner Bros Wabbitz"], ["Funk Anthem","MoneyBin Blues"],
               ["Chill Groove","Soylent Running"], ["Encore","Weasel! goes he Pop!"]]
aggregateSpec1 = [[pllBandMembers, "vocalist"],[nicknames, "Dewey", ],[pllInstruments, "Warner Bros Rabbit"], [pllMusicPieces, "Encore"]]
aggregateSpec2 = [[pllBandMembers, "vocalist"], [pllBandMembers, "drummer"], [pllBandMembers,"lead guitar"], [pllBandMembers, "bass player"]]
aggregateSpec3 = [[nicknames, pt.parseLineID], [pllBandMembers, pt.parseLineID], [pllInstruments,pt.parseLineID],
                  [pllMusicPieces, pt.parseLineID]]
aggregateSpec4 = [[nicknames,"Phred"],[pllMusicPieces, "Set Opener"], [pllInstruments, "Moneybin Blues"],
                [pllInstruments, "Soylent Running"],[pllInstruments,"Weasel! goes the Pop!"], [pllMusicPieces, "Chill Groove"],
                [pllMusicPieces, "Set Opener"], [pllMusicPieces,"Funk Anthem"]]

def unittest_Aggregator_buildSourceMaps():
    ## test the Aggregator sourceMap class
    srcMap1 = aggr.dataAggregator.sourceMap(pllBandMembers)
    srcMap2 = aggr.dataAggregator.sourceMap(aggregateSpec2, )
    # build map

    return False