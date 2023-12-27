import value as g

def plugin_patch(patch):

    if patch == "giantFlange":
        g.command_diff = g.command_diff + ",1"
    elif patch == "fmOsc":
        if g.command_diff == "plugin=fm_osc_1415 label=fmOsc control=1.0":
            g.command_diff = "plugin=fm_osc_1415 label=fmOsc control=2.0"
    elif patch == "djFlanger":
        g.command_diff = g.command_diff.replace("control=", "control=1.0,")
    elif patch == "vocoder":
        g.command_diff = g.command_diff.replace("control=0.0", "control=1.0")
    elif patch == "sine_faaa":
        g.command_diff = g.command_diff.replace("control=", "control=\"Unable to set parameters\"")

