# aiMove.py
# various movement AI scripts for mobs

import random
import World, Globals






#---------------------------------------------------------

class movementAI:
	def __init__(self, mob, time):
		self.mob = mob
		self.time = time
		self.Timer = World.Timer(Globals.MoveTIMERS, self.time, None, None, self, True)
		

	def selector(self, oddsList):     # pick a random selection from an odds list and return it.
                            # an odds list is a list containing any number of smaller lists, each with the format of [<choice>,<odds value>]
	    totalOdds = 0

	    for sel in oddsList:
	        totalOdds += sel[1]

	    oddSum = 0
	    selection = random.randint(0, totalOdds)
	    for sel in oddsList:
	        oddSum += sel[1]
	        if oddSum >= selection:
	            break
	    # print sel
	    return sel

	def introvertRandom(self, args):		# randomly chooses an exit, and takes it.  Much greater chances of moving when mobs of the same type are in the room.
		odds = 1					# Essentially, these mobs flee other mobs of their own type.  They want to find their own room.
		for mob in self.mob.currentRoom.mobs:
			odds +=1
		#check if mob should move
		oddsList = [[True, odds], [False, 2]]	#basic 50/50 odds to move with one other mob present, with the odds increasing as the number of mobs in the room goes up
		winner = self.selector(oddsList)
		#if mob should move, select a random exit and move there
		# if self.mob.currentRoom != None:
		# 	print "  moveCheck - " + str(self.mob.name) +"["+ str(self.mob.currentRoom.region) + ":" + str(self.mob.currentRoom.name) +"]" + " " + str(winner)
		# else:
		# 	print "  moveCheck - " + str(self.mob.name) + " " + str(winner)
		if winner[0] == 'True' or winner[0] == True:
			if self.mob.currentRoom != None:
				randRange = len(self.mob.currentRoom.exits) - 1
				selection = random.randint(0, randRange)
				exitList = []
				for exit in self.mob.currentRoom.exits:
					exitList.append(exit)
				# print exitList

				selectedExit = exitList[selection]

				for room in Globals.regionListDict[self.mob.currentRoom.region]:
					if Globals.regionListDict[self.mob.currentRoom.region][room].name == selectedExit:
						newRoom = Globals.regionListDict[self.mob.currentRoom.region][room]

				for player in self.mob.currentRoom.players:
					player.client.send_cc("^y%s left.^~\n" %self.mob.name.capitalize())

				oldMobRoom = self.mob.currentRoom

				if newRoom != None:
					self.mob.currentRoom.mobs.remove(self.mob)
					self.mob.currentRoom = newRoom
					newRoom.mobs.append(self.mob)

				print "Mm " + str(self.mob) + " " + str(self.mob.name) + ": from [" + str(oldMobRoom.region) +":"+ str(oldMobRoom.name) + "] to [" + str(self.mob.currentRoom.region) +":"+ str(self.mob.currentRoom.name) + "]"

				for player in self.mob.currentRoom.players:
					player.client.send_cc("^yA %s has entered.^~\n" %self.mob.name)

		self.resetTimer()

	def extrovertRandom(self, args):		# randomly chooses an exit, and takes it.  Much greater chances of moving when there are no other mobs of the same type in the room.
		odds = 0					# this AI tends to cause mobs to 'clump up' in a room, with them being less prone to leaving a room the more mobs of the same type that arrive.
		for mob in self.mob.currentRoom.mobs:
			if mob.name == self.mob.name:
				odds +=1
		#check if mob should move
		oddsList = [[True, 2], [False, odds]]	#basic 50/50 odds to move when one other mob is present, with the odds decreasing as the number of mobs in the room of the same type goes up
		winner = self.selector(oddsList)
		#if mob should move, select a random exit and move there
		# if self.mob.currentRoom != None:
		# 	print "  moveCheck - " + str(self.mob.name) +"["+ str(self.mob.currentRoom.region) + ":" + str(self.mob.currentRoom.name) +"]" + " " + str(winner)
		# else:
		# 	print "  moveCheck - " + str(self.mob.name) + " " + str(winner)
		if winner[0] == 'True' or winner[0] == True:
			if self.mob.currentRoom != None:
				randRange = len(self.mob.currentRoom.exits) - 1
				selection = random.randint(0, randRange)
				exitList = []
				for exit in self.mob.currentRoom.exits:
					exitList.append(exit)
				# print exitList

				selectedExit = exitList[selection]

				for room in Globals.regionListDict[self.mob.currentRoom.region]:
					if Globals.regionListDict[self.mob.currentRoom.region][room].name == selectedExit:
						newRoom = Globals.regionListDict[self.mob.currentRoom.region][room]

				for player in self.mob.currentRoom.players:
					player.client.send_cc("^y%s left.^~\n" %self.mob.name.capitalize())

				oldMobRoom = self.mob.currentRoom

				if newRoom != None:
					self.mob.currentRoom.mobs.remove(self.mob)
					self.mob.currentRoom = newRoom
					newRoom.mobs.append(self.mob)

				print "Mm " + str(self.mob) + " " + str(self.mob.name) + ": from [" + str(oldMobRoom.region) +":"+ str(oldMobRoom.name) + "] to [" + str(self.mob.currentRoom.region) +":"+ str(self.mob.currentRoom.name) + "]"

				for player in self.mob.currentRoom.players:
					player.client.send_cc("^yA %s has entered.^~\n" %self.mob.name)

		self.resetTimer()


	def doNotMove(self, args):		# don't ever move from the room the mob spawned in
		self.resetTimer()


	def basicRandom(self, args):	# randomly choose an exit, and take it.  Unaffected by number of mobs in the room, always 50/50 chance of moving
		oddsList = [[True, 4], [False, 1]]
		#print self.mob.currentRoom	
		winner = self.selector(oddsList)
		#if mob should move, select a random exit and move there
		# print self.mob
		# print Globals.mobsFromFile
		# print self.mob.currentRoom
		# if self.mob.currentRoom != None:
		# 	print "  moveCheck - " + str(self.mob.name) +"["+ str(self.mob.currentRoom.region) + ":" + str(self.mob.currentRoom.name) +"]" + " " + str(winner)
		# else:
		# 	print "  moveCheck - " + str(self.mob.name) + " " + str(winner)
		if winner[0] == 'True' or winner[0] == True:
			# print "winner"
			# print self.mob.currentRoom
			if self.mob.currentRoom != None:
				newRoom = None
				# print "has room"
				randRange = len(self.mob.currentRoom.exits) - 1
				selection = random.randint(0, randRange)
				exitList = []
				for exit in self.mob.currentRoom.exits:
					exitList.append(exit)
				# print exitList

				selectedExit = exitList[selection]

				for room in Globals.regionListDict[self.mob.currentRoom.region]:
					if Globals.regionListDict[self.mob.currentRoom.region][room].name == selectedExit:
						newRoom = Globals.regionListDict[self.mob.currentRoom.region][room]
				
				for player in self.mob.currentRoom.players:
					player.client.send_cc("^y%s left.^~\n" %self.mob.name.capitalize())

				oldMobRoom = self.mob.currentRoom

				if newRoom != None:
					self.mob.currentRoom.mobs.remove(self.mob)
					self.mob.currentRoom = newRoom
					newRoom.mobs.append(self.mob)


				# print oldMobRoom
				# print self.mob.currentRoom
				print "Mm " + str(self.mob) + " " + str(self.mob.name) + ": from [" + str(oldMobRoom.region) +":"+ str(oldMobRoom.name) + "] to [" + str(self.mob.currentRoom.region) +":"+ str(self.mob.currentRoom.name) + "]"

				for player in self.mob.currentRoom.players:
					player.client.send_cc("^yA %s has entered.^~\n" %self.mob.name)

		self.resetTimer()

	def resetTimer(self):
		self.Timer.currentTime = self.time
		# print "resetTimer:" + str(self.Timer) + " " + str(self.Timer.currentTime) + " " + str(self.mob)
		# print Globals.mobsFromFile
		# found = False
		# for mob in Globals.mobsFromFile:
		# 	if mob == self.mob:
		# 		found = True
		# 		print "found " + str(self.mob) + " " + str(mob) 
		# if found == False:
		Globals.MoveTIMERS.append(self.Timer)
		# print "self.mob appended"
		# print Globals.MoveTIMERS