#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ,--(saket)--(RiPlayServer)--(01/07/16 09:40)--(【ツ】)---
# `--(~/player.py$)-->

import json
import os
import signal
import subprocess
import threading
from random import shuffle

import api
from main import log


__author__ = 'saket'
__tag__ = 'main'

source = None
player = None

_music_dir = "/home/pi/Music"
_player_lock = threading.Lock()
_player_thread = None
_stop_requested = False
_collection = None
_playlist = []


def _start_player():
    """Play all items found on Playlist sequentially on Radio.

    Starts player and radio process. Waits for the processes to end.
    Returns if _stop_requested or playlist is empty
    """
    global source, player, _stop_requested

    _player_lock.acquire()
    while _playlist:
        try:
            log.info("Playing : %s" % _playlist[0])
            # avconv -i "$File" -f s16le -ar 44100 -ac 2 -loglevel panic -
            source = subprocess.Popen(
                    ["avconv", "-i", "%s/%s" % (_music_dir, _playlist[0]), "-f", "s16le", "-ar", "44100", "-ac", "2", "-loglevel",
                     "panic", "-"],
                    stdout=subprocess.PIPE)

            # aplay -c 2 -f cd -q
            player = subprocess.Popen(["aplay", "-c", "2", "-f", "cd", "-q"],
                                      stdin=source.stdout)

            source.stdout.close()
        except Exception as error:
            log.error("Error: %s" % error.message)

        if player:
            log.debug("player.wait() :)")
            player.wait()
            log.debug("Player terminated :)")
        if source:
            log.debug("source.wait() :)")
            source.wait()
            log.debug("Source terminated :)")

        if _stop_requested:
            _stop_requested = False
            break

        _playlist.pop(0)

    source = None
    player = None

    _player_lock.release()
    log.info("Thread terminated :)")


def _stop_player_process():
    """Stop both Radio and Player processes.

    Does not remove current playing song from playlist. User assumes responsibility of managing playlist.
    Acts like pressing STOP on any media player.
    """
    if player and player.poll() is None:
        player.terminate()
        log.debug("Terminating player process :)")

    if source and source.poll() is None:
        source.terminate()
        log.debug("Terminating source process :)")


def start_player(force=False):
    """Start playing music from playlist.

    Creates a thread to act as Player thread to play from playlist.
    Returns if playlist is empty or player is running and not forced.

    :type force:bool Should forcefully stop player
    """
    if not _playlist:
        return

    global _player_thread
    if _player_thread and _player_thread.isAlive():
        if force:
            # Player needs to be restarted
            stop_player()
        else:
            # Player is already running
            return

    _player_thread = threading.Thread(target=_start_player)
    _player_thread.start()


def stop_player():
    """Stops player without removing currently playing song"""
    global _stop_requested
    _stop_requested = True
    _stop_player_process()


def skip():
    """Skip currently playing music. Stops player which removes currently playing song"""
    _stop_player_process()


def clear():
    """Clear current playlist"""
    global _playlist
    if _player_thread and _player_thread.isAlive():
        del _playlist[1:]
    else:
        _playlist = []


def play(position):
    """Play item at position in collection as new playlist"""
    global _playlist
    collection = get_collection()
    if position == "all":
        _playlist = [collection[k] for k in collection]
    elif position == "shuffle":
        _playlist = [collection[k] for k in collection]
        shuffle(_playlist)
    elif position in collection:
        _playlist = [collection[position]]
    else:
        log.error("Play requested for %r" % position)

    start_player(True)


def pause():
    """Pause currently running source"""
    global source
    if source:
        os.kill(source.pid, signal.SIGSTOP)


def conti():
    """Continue source"""
    global source
    if source:
        os.kill(source.pid, signal.SIGCONT)


def queue(position):
    """Add item at position in collection to playlist"""
    global _playlist
    collection = get_collection()
    _playlist.append(collection[position])
    log.info("Adding : %s" % collection[position])
    start_player()


def get_collection():
    """
    Read files available and return list of multimedia files available
    :return: dict of files
    :rtype dict
    """
    global _collection
    if _collection:
        return _collection

    try:
        _collection = {i + 1: x for i, x in enumerate(os.listdir(_music_dir))}
        return _collection

    except OSError as err:
        log.error(err.message)
        return {}


def get_collection_json():
    """Get complete Collection(dict) as JSON object"""
    return json.dumps(get_collection())


def get_playlist():
    """Get current playlist as list"""
    return _playlist


def get_playlist_json():
    """Get current playlist as JSON object"""
    return json.dumps(get_playlist())


def get_status():
    if source and source.poll() is None:
        keys = _collection.keys()
        return {'playing': True,
                'name': _playlist[0],
                'index': keys[_collection.values().index(_playlist[0])],
                'queued': len(_playlist) - 1
                }

    return {'playing': False,
            'queued': len(_playlist)
            }


def get_status_json():
    return json.dumps(get_status())
