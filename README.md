# !!!!! Fork updated to May 2025 !!!!!
This fork of lociii original work was made for those of us who wants to keep it simple without having this overwolf plugin software running and keeping the original CS2 integration by webhook directly to our homeassistant...
It updates the relevant parts that got broke in May 2025 update of home assistant.
Added an example of updated scripts/automation to use.


# CS:GO game state integration for Home Assistant

## What is this about?

[Home Assistant](https://www.home-assistant.io/) is an open source home automation and control system.

[Counter-Strike: Global Offensive](https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/) is a tactical first person shooter by Valve Corporation

## What does it do?

This integration [listens to game state changes](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) and fires relevant events in Home Assistant. These can then be used to change your lighting or start some fireworks :-)

Convert your desk into a big Counter-Strike tournament stage!

Please read [info.md](info.md) carefully to understand how this integration is set up and connected to your Counter-Strike client.

## How can I install it?

The easiest way to install the integration is by using [Home Assistant Community Store HACS](https://hacs.netlify.com/).
Just search for "csgo" and install the integration. Further instruction are shown in the integration description in HACS.
