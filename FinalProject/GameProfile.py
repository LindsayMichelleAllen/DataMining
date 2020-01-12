class GameProfile:
    gameId = 123456789
    title = 'Proposed Game'
    attributes = ['Post-apocalyptic', 'RPG', 'First-Person', 'First Person Shooter', 'FPS', \
        'Third-Person', 'Third Person Shooter', 'Shooter', 'Violent', 'Action', 'Puzzle', \
        'Magic', 'Sci-fi', 'Scifi', 'Single Player', 'Adventure', 'Large Map', 'Open World', \
        'Horror', 'Free', 'Free To Play', 'Male Lead', 'Female Lead', 'Indie']
    projectedSuccessScore = 0

    def printProfile(self, f):
        f.write("\n----------------------------------------------------------------------------")
        f.write("\nTitle: " + self.title)
        f.write("\nGame ID: " + str(self.gameId))
        f.write("\nAttributes:\n")
        count = 0
        temp = ''
        for attr in self.attributes:
            temp += attr + " | "
            count += 1
            if count == 5:
                count = 0
                temp += '\n'
        f.write(str(temp))

            
        f.write("\n----------------------------------------------------------------------------\n")

