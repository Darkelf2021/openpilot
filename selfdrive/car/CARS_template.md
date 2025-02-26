{% set footnote_tag = '[<sup>{}</sup>](#footnotes)' -%}
{% set star_icon = '<a href="##"><img valign="top" src="assets/icon-star-{}.svg" width="22" /></a>' -%}

# Supported Cars

A supported vehicle is one that just works when you install a comma device. Every car performs differently with openpilot, but all supported cars should provide a better experience than any stock system.

## How We Rate The Cars

{% for star_row in star_descriptions.values() %}
{% for name, stars in star_row.items() %}
### {{name}}
{% for star, description in stars %}
- {{star_icon.format(star)}} - {{description}}
{% endfor %}

{% endfor %}
{% endfor %}

# {{all_car_info | length}} Supported Cars

|{{Column | map(attribute='value') | join('|')}}|
|---|---|---|:---:|:---:|:---:|:---:|
{% for car_info in all_car_info %}
|{% for column in Column %}{{car_info.get_column(column, star_icon, footnote_tag)}}|{% endfor %}

{% endfor %}

<a id="footnotes"></a>
{% for footnote in footnotes %}
<sup>{{loop.index}}</sup>{{footnote}} <br />
{% endfor %}

## Community Maintained Cars
Although they're not upstream, the community has openpilot running on other makes and models. See the 'Community Supported Models' section of each make [on our wiki](https://wiki.comma.ai/).

# Don't see your car here?

**openpilot can support many more cars than it currently does.** There are a few reasons your car may not be supported.
If your car doesn't fit into any of the incompatibility criteria here, then there's a good chance it can be supported! We're adding support for new cars all the time. We don't have a roadmap for car support, and in fact, most car support comes from users like you!

### Which cars are able to be supported?

openpilot uses the existing steering, gas, and brake interfaces in your car. If your car lacks any one of these interfaces, openpilot will not be able to control the car. If your car has any form of [LKAS](https://en.wikipedia.org/wiki/Automated_Lane_Keeping_Systems)/[LCA](https://en.wikipedia.org/wiki/Lane_centering) and [ACC](https://en.wikipedia.org/wiki/Adaptive_cruise_control), then it almost certainly has these interfaces. These interfaces generally started shipping on cars around 2016.

If your car has the following packages or features, then it's a good candidate for support. If it does not, then it's unlikely able to be supported.

| Make | Required Package/Features |
| ---- | ------------------------- |
| Acura | Any car with AcuraWatch Plus will work. AcuraWatch Plus comes standard on many newer models. |
| Honda | Any car with Honda Sensing will work. Honda Sensing comes standard on many newer models. |
| Subaru | Any car with EyeSight will work. EyeSight comes standard on many newer models. |
| Nissan | Any car with ProPILOT will likely work. |
| Toyota & Lexus | Any car that has Toyota/Lexus Safety Sense with "Lane Departure Alert with Steering Assist (LDA w/SA)" and/or "Lane Tracing Assist (LTA)" will work. Note that LDA without Steering Assist will not work. These features come standard on most newer models. |
| Hyundai, Kia, & Genesis | Any car with Smart Cruise Control (SCC) and Lane Following Assist (LFA) or Lane Keeping Assist (LKAS) will work. LKAS/LFA comes standard on most newer models. Any form of SCC will work, such as NSCC. |
| Chrysler, Jeep, & Ram | Any car with LaneSense and Adaptive Cruise Control will likely work. These come standard on many newer models. |

### FlexRay

All the cars that openpilot supports use a [CAN bus](https://en.wikipedia.org/wiki/CAN_bus) for communication between all the car's computers, however a CAN bus isn't the only way that the cars in your computer can communicate. Most, if not all, vehicles from the following manufacturers use [FlexRay](https://en.wikipedia.org/wiki/FlexRay) instead of a CAN bus: **BMW, Mercedes, Audi, Land Rover, and some Volvo**. These cars may one day be supported, but we have no immediate plans to support FlexRay.

### Toyota Security

Specific new Toyota models are shipping with a new message authentication method that openpilot does not yet support.
So far, this list includes:
* Toyota Rav4 Prime 2022+
* Toyota Sienna 2021+
* Toyota Venza 2021+
* Toyota Sequoia 2023+
* Toyota Tundra 2022+
* Toyota Yaris 2022+
* Toyota Corolla Cross (only US model)
* Lexus NX 2021+
