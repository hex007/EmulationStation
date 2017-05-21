#pragma once

#include <memory>
#include <string.h>

class AudioPlayer
{
private:
	AudioPlayer(){};

public:
	~AudioPlayer(){};

	static void start();
	static void stop();
	static void skip();
	static void pause();
	static void conti();
	static void clear();
	static void play(int song);
	static void queue(int song);
};
