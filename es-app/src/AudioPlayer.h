#pragma once

#include <memory>
#include <string.h>

/*!
Singleton pattern. Call getInstance() to get an object.
*/
class AudioPlayer
{
private:
	// Internal variables here
	static std::weak_ptr<AudioPlayer> sInstance;

	AudioPlayer(){};
	AudioPlayer(const AudioPlayer & right);
	AudioPlayer & operator=(const AudioPlayer & right);

public:
	static std::shared_ptr<AudioPlayer> & getInstance();
	~AudioPlayer(){};

	void start();
	void stop();
	void skip();
	void pause();
	void conti();
	void clear();
	void play(int song);
	void queue(int song);
};
