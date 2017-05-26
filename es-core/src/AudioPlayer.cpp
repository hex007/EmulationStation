#include "AudioPlayer.h"

void AudioPlayer::play(int song){
	switch (song){
		case -2:
			// Shuffle
			system("curl -s http://localhost:8080/api/play/shuffle > /dev/null");
			break;
		case -1:
			// Ordered
			system("curl -s http://localhost:8080/api/play/all > /dev/null");
			break;
		default:
			std::string command = std::string("curl -s http://localhost:8080/api/play/") + std::to_string(song) + std::string(" > /dev/null");
			system(command.c_str());
	}
}

void AudioPlayer::queue(int song){
	if (song < 0)
		return;

	std::string command = std::string("curl -s http://localhost:8080/api/queue/") + std::to_string(song) + std::string(" > /dev/null");
	system(command.c_str());
}

void AudioPlayer::start(){
	system("curl -s http://localhost:8080/api/start > /dev/null");
}

void AudioPlayer::stop(){
	system("curl -s http://localhost:8080/api/stop > /dev/null");
}

void AudioPlayer::skip(){
	system("curl -s http://localhost:8080/api/skip > /dev/null");
}

void AudioPlayer::clear(){
	system("curl -s http://localhost:8080/api/clear > /dev/null");
}

void AudioPlayer::pause(){
	system("curl -s http://localhost:8080/api/pause > /dev/null");
}

void AudioPlayer::conti(){
	system("curl -s http://localhost:8080/api/continue > /dev/null");
}
