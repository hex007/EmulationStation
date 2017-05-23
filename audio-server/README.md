# RaspberryPi Radio Player Interface

A simple API handling server for PiFM to control Raspberry Pi fm transmission. Can be easily extended to serve web pages or to be controlled using buttons connected to GPIO pins for standalone function. 

Since Python has an easily modifiable server, this was easy and helpful.


Tested with **RaspberryPi v1 model B and Zero**. For others just update the pifm binary with a working one and change command line for pifm in player.py

    player = subprocess.Popen(["./pifm_binary_name", parameters...], stdin=player.stdout)
    
To test pifm try:

    avconv -i MUSIC_FILE s16le -ar 22.05k -ac 1 - | sudo ./pifm - FREQ


#### Changes in latest version (13 July 2016):
- Support for subscription to player status updates
- Working Android controller application ([RiPlay for Android](https://github.com/hex007/pifm_client_android))
- Switch between radio and audio playback (restarts song)


#### Features todo:
- Volume control
    - ALSA volume control (should be simple)
    - Multithreaded pifm to change volume on the fly


#### Install instruction (on RPi a.k.a. Server):

    # Install avconv 
    sudo apt-get update
    sudo apt-get install libav-tools

    # Get Server code
    git clone https://github.com/hex007/pifm_server
    cd pifm_server
    g++ -O3 -o pifm pifm.c
    mkdir Music
    # copy music files to Music/

    # Start server
    sudo python main.py


#### Optional: Start server at startup

    # To start server at startup:
    sudo nano /etc/rc.local

    # In nano INSERT BEFORE return 0
    cd /home/pi
    sudo python main.py > latest.log &


#### API Documentation

Using a client to send requests to Server

1. Get Music Collection : returns JSONobject

        curl http://raspberrypi.local:8080/api/collection

        # For formatted Collection ->
        curl http://raspberrypi.local:8080/api/collection | sed "s|\", \"|\"\\n\"|g"

2. Get playlist : returns JSONarray

        curl http://raspberrypi.local:8080/api/playlist

3. Get Broadcast Frequency

        curl http://raspberrypi.local:8080/api/freq

4. Play X = [N|all|shuffled] from Collection

        curl http://raspberrypi.local:8080/api/play/X

5. Queue X = [N|all|shuffled] from Collection

        curl http://raspberrypi.local:8080/api/queue/X

6. Stop player, leave queue as playlist

        curl http://raspberrypi.local:8080/api/stop

7. Start player, continue with playlist

        curl http://raspberrypi.local:8080/api/start

8. Skip song in playlist

        curl http://raspberrypi.local:8080/api/skip

9. Clear playlist; keeps current song if playing

        curl http://raspberrypi.local:8080/api/clear


#### Subscription management

Changes in the player state can be subscribed to using:

     curl http://raspberrypi.local:8080/api/subscribe?port=$PORT

Once a user is subscribed to the player, every state change is reported to the subscriber at the
 port requested `$PORT`. The IP address is the same as the one requesting the subscription .The
 client machine must have a server running to accept status updates. If the status update request
 from the RPi to client fails then the client is automatically unsubscribed from the stats updates.

To manually request for unsubscription send request:

    curl http://raspberrypi.local:8080/api/unsubscribe


#### Switch outputs

Audio output (defaults to radio) can be changed using the following requests:

    # To set output as Audio (3.5mm Jack or HDMI)
    curl http://raspberrypi.local:8080/api/output/audio

    # To set output as Radio (PiFM)
    curl http://raspberrypi.local:8080/api/output/radio

Multiple attempts at switching causes RPi to output noise and a reboot is needed to resolve the issue.