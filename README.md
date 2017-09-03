# trafficrobot README

This project is my trafficrobot. All it does is fetch traffic data from
the [Traffic England](http://www.trafficengland.com/) web site, filter
out the bits I might be interesgted in, and then push the results to my
phone via [Pushover](http://www.pushover.net/). I built this to scratch
my own itch, and so it's really not a good example of anything. I'm
putting it up here in the vague hope that I might actually do proper
versioning on it, rather than having lots of files with a date in the
filename. Do let me know if it's any use to you.

NB: There are *many* things hardwired into the code. I'm working
on removing this stuff as I find it. Like I said, this is vaguely
productionised version of something I built to be a MVP for me, and then
welded a few other bits on.  Sorry about that.

# Dependencies

I use a library called `chump` to do the actual talking to Pushover. It
seems to fail occasionally, but I haven't got around to working out why,
mainly because it doesn't alert properly when there's a Pushover failure.
I should probably fix that.

## Support files

| File                       | Purpose                                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------------------- |
| app-api-key.example        | Your actual Pushover App API key goes in here                                                   |
| lastguid.example           | Code stores the last GUID seen in a file called `lastguid.txt` to prevent duplicate alerts      |
| trafficrobot-users.example | User details (user API keys and so on) stored in `trafficrobot-users.txt` to be used for alerts |

Further documentation is in the files themselves. NB: they should have
the extension `.example` replaced with `.txt` to run. Or you could edit
the `get_fileloc` function which does the mapping from internal reference
to file name.  But I'd suggest putting the correct stuff in files called
`something.txt` using the `.example` ones as templates.

## Pushover

See the instuctions at [the Pushover website](http://www.pushover.net/)
for more iformation on how to configure Pushover for your requirements.

## Chump

Chump is also on github [here](https://github.com/karanlyons/chump).
It needs two keys to use, which you can get from Pushover. I've removed
my API keys from this version, you'll need to substute yours in to make
it work for you.

I have had some problems with Chump, but then I haven't tested against
the latest version, so I should probably do that.

See
[the instructions in that project](https://github.com/karanlyons/chump).
for information on how to set Chump up.

