# Import the perl module so we can call the SPADS Plugin API
import perl
import traceback
import sys
import json
import base64
import zlib
import os
import time

# perl.BarManager is the Perl representation of the BarManager plugin module
# We will use this object to call the plugin API
spads=perl.BarManager

#------------------ Instance global "constants" -------------

BMP = "BarManager|"

SpringCrashInfologPatterns = ['Spring: caught content_error:'] # add any text here that we would like to catch as a crash, preferably, this should be in the barmanager config though
CrashDir = ""

DBGLEVEL = 3

pluginParams = {}
#---------------- Battleroom Variables to Track --------------
AisPresent = {} # dunno the format yet, should support script tags to set AI profiles
isBattleLocked = False
BattleState = {}



spadsConf = None #  {'lobbyReconnectDelay': 15, 'banList': 'empty', 'mapLink': 'http://springfiles.com/search_result.php?search=%m&select=select_all', 'promoteMsg': '%pplayer(s) needed for battle "%b" [%o, %a] (%u)', 'autoLock': 'off', 'lobbyPassword': 'petike', 'lobbyFollowRedirect': '1', 'lobbyHost': 'bar.teifion.co.uk', 'allowedLocalAIs': 'E323AI;HughAI;KAIK;RAI', 'logGameChat': '1', 'msgFloodAutoKick': '15;7', 'masterChannel': 'autohosts', 'allowGhostMaps': '0', 'maxBots': '16', 'lobbyInterfaceLogLevel': '5', 'opOnMasterChannel': '0', 'teamSize': 6, 'lobbyPort': '8200', 'commandsFile': 'commands.conf', 'unlockSpecDelay': '5;30', 'logPvChat': '1', 'extraBox': '0', 'alertDuration': '72', 'privacyTrustLevel': '130', 'springServer': '/home/eru/spads/var/spring/spring_bar_.BAR.104.0.1-1956-g0092498_linux-64-minimal-portable/spring-headless', 'simpleEventLogLevel': '5', 'springDataDir': '/home/eru/spads/var/spring/data', 'autoBlockColors': '0', 'autoManagedSpringDir': '/home/eru/spads/var/spring', 'rotationManual': 'random', 'rotationType': 'map;certified', 'defaultPreset': 'team', 'spoofProtection': 'warn', 'minPlayers': 1, 'welcomeMsgInGame': 'Hi %u (%d), welcome to %n .', 'shareId': '', 'autoCallvote': '1', 'ircColors': '0', 'voteMode': 'normal', 'autoStart': 'on', 'reCallVoteDelay': 10, 'springServerType': 'headless', 'promoteChannels': 'main', 'autoHostPort': '53199', 'welcomeMsg': 'Hi %u (%d), welcome to %n .', 'maxAutoHostMsgLength': '240', 'rotationEndGame': 'off', 'logBattleJoinLeave': '1', 'cmdFloodAutoIgnore': '8;8;4', 'pluginsDir': '/home/eru/spads/var/plugins', 'autoSpecExtraPlayers': '1', 'autoLearnMaps': '1', 'voteTime': 45, 'springConfig': '', 'description': 'Team Game Global Settings', 'advertDelay': '15', 'logChanChat': '0', 'kickFloodAutoBan': '5;120;5', 'dataDumpDelay': 60, 'clanMode': 'tag(5);pref(5)', 'nbTeams': 2, 'rotationEmpty': 'random', 'alertDelay': '6', 'lobbyLogin': '[teh]host15', 'botsRank': '3', 'hostingPreset': 'enginetesting', 'noSpecDraw': '0', 'autoManagedSpringVersion': '', 'battlePreset': 'team', 'autoAddBotNb': 0, 'freeSettings': 'autoLock;teamSize(1-8)', 'maxSpecs': '', 'colorSensitivity': 55, 'autoReloadArchivesMinDelay': 30, 'endGameAwards': '1', 'ghostMapLink': 'http://springfiles.com/search_result.php?search=%m&select=select_all', 'broadcastChannels': 'autohosts', 'maxChatMessageLength': 1024, 'logDir': '/home/eru/spads/var/spads_host15/log', 'autoBlockBalance': '1', 'autoHostInterfaceLogLevel': '5', 'hideMapPresets': '0', 'kickBanDuration': '300', 'maxBytesSent': 49000, 'logBattleChat': '1', 'useWin32Process': '0', 'map': 'Comet Catcher Remake 1.8', 'allowMapOptionsValues': '1', 'autoSaveBoxes': '2', 'voteRingDelay': '0', 'allowModOptionsValues': '1', 'eventModel': 'auto', 'promoteDelay': '600', 'maxLocalBots': '16', 'votePvMsgDelay': '0', 'maxRemoteBots': '16', 'statusFloodAutoKick': '24;8', 'userDataRetention': '-1;-1;-1', 'autoSetVoteMode': '1', 'logGameServerMsg': '1', 'instanceDir': '/home/eru/spads/var/spads_host15', 'maxLowPrioBytesSent': 48000, 'allowSettingsShortcut': '1', 'autoStop': 'gameOver', 'skillMode': 'TrueSkill', 'rankMode': 'account', 'localLanIp': '192.168.1.102', 'minTeamSize': '1', 'rotationDelay': 600, 'idShareMode': 'off', 'logChanJoinLeave': '0', 'forceHostIp': '', 'spadsLogLevel': '5', 'autoLockClients': 64, 'endGameCommandEnv': '', 'speedControl': '2', 'endGameCommand': '', 'autoLoadPlugins': 'BarManager;AutoRegister;JsonStatus;InGameMute', 'restoreDefaultPresetDelay': '30', 'springieEmulation': 'warn', 'logGameJoinLeave': '1', 'sendRecordPeriod': 5, 'noSpecChat': '0', 'autoLockRunningBattle': '0', 'balanceMode': 'clan;skill', 'updaterLogLevel': '5', 'varDir': '/home/eru/spads/var', 'midGameSpecLevel': '0', 'handleSuggestions': '0', 'unitsyncDir': '/home/eru/spads/var/spring/spring_bar_.BAR.104.0.1-1956-g0092498_linux-64-minimal-portable/', 'endGameCommandMsg': '', 'etcDir': '/home/eru/spads/etc', 'localBots': 'joe 0 E323AI;jim core#FF0000 KAIK', 'minRingDelay': '20', 'minVoteParticipation': '50', 'advertMsg': '', 'maxChildProcesses': '32', 'autoRestartForUpdate': 'off', 'forwardLobbyToGame': '1', 'nbPlayerById': 1, 'autoLoadMapPreset': '0', 'autoFixColors': 'advanced', 'preset': 'team', 'alertLevel': 130, 'autoBalance': 'advanced', 'maxSpecsImmuneLevel': '100', 'floodImmuneLevel': 100, 'autoUpdateRelease': '', 'mapList': 'all', 'autoUpdateDelay': '300'}


#------------------ JSON OBJECT INFO ------------------
# Each json string will contain a dict, for example, for a votestart
#

# This is the first version of the plugin
pluginVersion='0.1'

# This plugin requires a SPADS version which supports Python plugins
# (only SPADS versions >= 0.12.29 support Python plugins)
requiredSpadsVersion='0.12.29'

# We define 2 global settings (mandatory for plugins implementing new commands):
# - commandsFile: name of the plugin commands rights configuration file (located in etc dir, same syntax as commands.conf)
# - helpFile: name of plugin commands help file (located in plugin dir, same syntax as help.dat)
globalPluginParams = {'crashDir':['notNull'], 'crashFilePattern': ['notNull'], 'crashFilesToSave':['notNull'], 'crashInfologPatterns':['notNull'], 'chobbyGuiSettings':['notNull'], 'barManagerDebugLevel':['notNull']}
					#{ 'commandsFile': ['BarManagerCmd.conf'],
					  # 'helpFile': ['BarManagerHelp.dat'] }
presetPluginParams = None


# This is how SPADS gets our version number (mandatory callback)
def getVersion(pluginObject):
	return pluginVersion

# This is how SPADS determines if the plugin is compatible (mandatory callback)
def getRequiredSpadsVersion(pluginName):
	return requiredSpadsVersion

# This is how SPADS finds what settings we need in our configuration file (mandatory callback for configurable plugins)
def getParams(pluginName):
	return [ globalPluginParams , presetPluginParams ]

def json_gzip_base64(toencode):
	return base64.b64encode(zlib.compress(json.dumps(toencode).encode("utf-8"))).decode()

def SendBattleState():
	try:
		barmanagermessage = BMP + json.dumps({"BattleStateChanged": BattleState})
		spads.sayBattle(barmanagermessage)
		spads.slog(barmanagermessage, DBGLEVEL)
	except Exception as e:
		spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)

def BattleStateChanged(changedKey, changedValue):
	try:
		if changedKey not in BattleState or (changedKey in BattleState and BattleState[changedKey] != changedValue):
			BattleState[changedKey] = changedValue
			SendBattleState()
		else:
			spads.slog("No change in battle state: %s:%s"%(changedKey,changedValue),3)


	except Exception as e:
		spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)

# This is the class implementing the plugin
class BarManager:

	# This is our constructor, called when the plugin is loaded by SPADS (mandatory callback)
	def __init__(self,context):
		
		# We declare our new command and the associated handler
		spads.addSpadsCommandHandler({'myCommand': hMyCommand})
		
		# We call the API function "slog" to log a notice message (level 3) when the plugin is loaded
		spads.slog("Plugin loaded (version %s)" % pluginVersion,3)
		if spads.get_flag("can_add_socket"):
			spads.slog("This plugin can use sockets",3)
		if spads.get_flag("can_fork"):
			spads.slog("This plugin can fork processes",3)
		if spads.get_flag("use_byte_string"):
			spads.slog("This plugin can uses byte strings",3)

		try:
			pluginParams = spads.getPluginConf()
			DBGLEVEL = int(pluginParams['barManagerDebugLevel'])
			spadsConf = spads.getSpadsConf()
			spads.slog("pluginParams = " + str(pluginParams),DBGLEVEL)
			CrashDir = os.path.join(spadsConf['varDir'],'log',pluginParams['crashDir'])
			if not os.path.exists(CrashDir):
				spads.slog("Created CrashDir"+CrashDir,DBGLEVEL)
				os.makedirs(CrashDir)
			else:
				spads.slog("OK:CrashDir already exists"+CrashDir,DBGLEVEL)

		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		
		
	# This is the callback called when the plugin is unloaded
	def onUnload(self,reason):

		# We remove our new command handler
		spads.removeSpadsCommandHandler(['myCommand'])

		# We log a notice message when the plugin is unloaded
		spads.slog("Plugin unloaded",3)

	
	def onBattleOpened(self):
		try:
			spads.slog("Battle Opened",3)
			#spads.queueLobbyCommand(["!preset coop","!map DSDR"])
			#spads.addTimer("initrandommap",5, 0, lambda : spads.queueLobbyCommand(["map Talus"]))
			#spads.addTimer("yell",5, 0, lambda : spads.sayPrivate("[teh]Beherith","hi"))
			
			#dump stuff for testing
			#spadsdir = dir(spads)
			#spads.slog(str(spadsdir),3)
			
			#confFull = spads.getSpadsConfFull()
			#spads.slog("maps=" + str(confFull.maps),3)
			
			#spads.slog(type(confFull),3)
			#spads.slog(str(confFull),3)
			#attrs = vars(confFull)
			#spads.slog(attrs,3)
			#attrs2 = dir(attrs)
			#spads.slog("attrdirdir:"+str(attrs2)+str(attrs.keys()),3)
			#for k in sorted(attrs.keys()):
			#	spads.slog("%s:%s"%(str(k),str(attrs[k])),3)
			#spadsconf = spads.getSpadsConf()
			#spadsconf['map'] = "TheRock_V2"
			a = None
			#b = a + 1 # this is just a try:except: test
			
			spadsConf = spads.getSpadsConf()
			spads.slog("Trying to print spads configuration:",3)

			#TODO: Init battlestatuschanged sanely!

			#spads.slog(str(spadsConf),3)
			
			
			
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)

	def onGameEnd(self, endGameData):
		# The \%endGameData parameter is a reference to a hash containing all the data stored by SPADS concerning the game that just ended.
		# TODO: Send all of this lovely endGameData dict as a base64 encoded json to the bot account called AutohostMonitor as a private message
		try:
			spads.slog("onGameEnd",3)
			spads.slog("endGameData" + str(endGameData),3)
			spads.sayPrivate('AutohostMonitor', 'endGameData ' + json_gzip_base64(endGameData))
			
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
	
	def onJoinBattleRequest(self,userName,ipAddr):
		# todo: send whole battle state to user
		try:
			spads.slog("onJoinBattleRequest:" + str(userName),3)
			SendBattleState() # TODO: not good, user doesnt get this yet (as he is not joined yet according to server!)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		return 0 # return 1 if the user isnt allowed to join (return string for reason)
		
	def onPresetApplied(self,oldPresetName,newPresetName):
		# todo: send the updated preset to all battle participants
		try:
			spads.slog("onPresetApplied: " + str(oldPresetName) + " -> " + str(newPresetName),3)
			BattleStateChanged('preset',newPresetName)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		
	def onPrivateMsg(self,userName,message):
		# todo: nothing yet
		try:
			spads.slog("onPrivateMsg: " + str([userName,message]),3)
			
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		return 0 # return 1 if dont want Spads core to parse this message
		
	def onVoteRequest(self,source,user,command,remainingVoters):
		# $source indicates the way the vote has been requested ("pv": private lobby message, "battle": battle lobby message, "chan": master lobby channel message, "game": in game message)
		# $user is the name of the user requesting the vote
		# \@command is an array reference containing the command for which a vote is requested
		# \%remainingVoters is a reference to a hash containing the players allowed to vote. This hash is indexed by player names. Perl plugins can filter these players by removing the corresponding entries from the hash directly, but Python plugins must use the alternate method based on the return value described below.
		try:
			spads.slog("onVoteRequest: " + ','.join(map(str,[source,user,command,remainingVoters])), 3)
			
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		return 1 # allow the vote, 0 for disallow
			
	def onVoteStart(self,user,command):
		# command is an array reference containing the command for which a vote is started
		try:
			spads.slog("onVoteStart: " + ','.join(map(str,[user,command])), 3)
			barmanagermessage = BMP+json.dumps({"onVoteStart" : {'user':user, 'command':command}})
			spads.sayBattle(barmanagermessage)
			spads.slog(barmanagermessage,3)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
	
	def onVoteStop(self,voteResult):
		# This callback is called each time a vote poll is stoped.
		# $voteResult indicates the result of the vote: -1 (vote failed), 0 (vote cancelled), 1 (vote passed)
		try:
			spads.slog("onVoteStop: voteResult=" + str(voteResult), 3)
			
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)

	
	def onSpringStop(self,springPid):
		# This callback is called each time the Spring process ends.
		try:
			spads.slog("onSpringStop: springPid=" + str(springPid),3)
			instanceDir = spadsConf["instanceDir"]
			# Check for spring has crashed, and save the script and the infolog.txt
			infologlines = open(instanceDir + "/log/infolog.txt").readlines()
			for line in infologlines:
				for pattern in pluginParams['crashInfologPatterns'].split('|'):
					if pattern in line:
						for crashFileToSave in pluginParams['crashFilesToSave'].split('|'):
							outf = open(os.path.join(CrashDir, pluginParams['crashFilePattern']%(int(time.time()), crashFileToSave)),'w')
							outf.write(''.join(open(os.path.join(instanceDir,'log',crashFileToSave)).readlines()))
							outf.close()

						break
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
	
	def onSpringStart(self,springPid):
		# This callback is called each time a Spring process is launched to host a game.
		try:
			spads.slog("onSpringStart: springPid=" + str(springPid),3)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
	
	def preGameCheck(self,force,checkOnly,automatic):
		# This callback is called each time a game is going to be launched, to allow plugins to perform pre-game checks and prevent the game from starting if needed.
		# $force is 1 if the game is being launched using !forceStart command, 0 else
		# $checkOnly is 1 if the callback is being called in the context of a vote call, 0 else
		# $automatic is 1 if the game is being launched automatically through autoStart functionality, 0 else
		# The return value must be the reason for preventing the game from starting (for example "too many players for current map"), or 1 if no reason can be given, or undef to allow the game to start.
		# todo: dont allow startpostype = (fixed or random) on maps with less start positions than players!
		try:
			spads.slog("preGameCheck: " + ','.join(map(str,[force,checkOnly,automatic])),3)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		return None #
	
	def postSpadsCommand(self,command,source,user,params,commandResult):
		# This callback is called each time a SPADS command has been called.
		# $command is the name of the command (without the parameters)
		# $source indicates the way the command has been called ("pv": private lobby message, "battle": battle lobby message, "chan": master lobby channel message, "game": in game message)
		# $user is the name of the user who called the command
		# \@params is a reference to an array containing the parameters of the command		
		# $commandResult indicates the result of the command (if it is defined and set to 0 then the command failed, in all other cases the command succeeded)
		# todo: say the results of the changed stuff in battle room
		try:
			spads.slog("postSpadsCommand: " + ','.join(map(str,[command,source,user,params,commandResult])),3)
			if command == "lock" :
				BattleStateChanged("locked","on")
			elif command == "unlock":
				BattleStateChanged("locked","off")
			elif command == "set": # autoLock|autoStart|autoBalance|autoFixColors|nbTeams|balanceMode|clanMode|locked|preset
				lowercommand = params[0].lower()
				if lowercommand == 'autobalance':
					BattleStateChanged("autoBalance", params[1])
				elif lowercommand == 'balancemode':
					BattleStateChanged("balanceMode", params[1])
				elif lowercommand == 'nbteams':
					BattleStateChanged("nbTeams", params[1])
				elif lowercommand == 'teamsize':
					BattleStateChanged("teamSize", params[1])



			elif command == "vote":

				if params[0] in ['yes','y','no','n','blank','b']:
					if params[0] == 'yes':
						pass


		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		return None #

	def preSpadsCommand(self,command,source,user,params):
		# This callback is called each time a SPADS command is called, just before it is actually executed.
		# $command is the name of the command (without the parameters)
		# $source indicates the way the command has been called ("pv": private lobby message, "battle": battle lobby message, "chan": master lobby channel message, "game": in game message)
		# $user is the name of the user who called the command
		# \@params is a reference to an array containing the parameters of the command
		# This callback must return 0 to prevent the command from being processed by other plugins and SPADS core, or 1 to allow it.
		try:
			spads.slog("preSpadsCommand: " + ','.join(map(str,[command,source,user,params])),3)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		return 1
	
	def filterRotationMaps(self,rotationMaps):
		try:
			spads.slog("filterRotationMaps: rotationMaps=" + str(rotationMaps),3)
			#for map in rotationMaps:
			#	spads.slog(str(str(map)),3)
		except Exception as e:
			spads.slog("Unhandled exception: " + str(sys.exc_info()[0]) + "\n" + str(traceback.format_exc()),0)
		
		return rotationMaps # The callback must return a reference to a new array containing the filtered map names

# This is the handler for our new command
def hMyCommand(source,user,params,checkOnly):

	# checkOnly is true if this is just a check for callVote command, not a real command execution
	if checkOnly :
		
		# MyCommand is a basic command, we have nothing to check in case of callvote
		return 1
	
	# Fix strings received from Perl if needed
	# This is in case Inline::Python handles Perl strings as byte strings instead of normal strings
	# (this step can be skipped if your Inline::Python version isn't afffected by this bug)
	user=spads.fix_string(user)
	for i in range(len(params)):
		params[i]=spads.fix_string(params[i])
		
	# We join the parameters provided (if any), using ',' as delimiter
	paramsString = ','.join(params)

	# We log the command call as notice message
	spads.slog("User %s called command myCommand with parameter(s) \"%s\"" % (user,paramsString),3)
