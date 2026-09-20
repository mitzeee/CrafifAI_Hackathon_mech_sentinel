"""
Faction materials, straight from the art bible section 5.

Combine = straight lines and smoke. Reedfolk = curves and glow. A player must
be able to call the faction from silhouette and colour alone, out of focus.

Render style is LOCKED (art bible section 2): faceted low-poly, flat shading,
untextured flat-colour materials, muted dusty earth palette. So these are the
final shipping colours, not placeholders -- the material IS the look.

Saturation is deliberately low and metalness deliberately restrained. In this
style a high-spec metal reads as a different game; the Combine's "metal" sells
through faceted silhouette and value contrast, not through reflections.
"""

from kit import mat


def combine():
    """Windward Combine: riveted, cut, bolted from machine detritus."""
    return dict(
        steel=mat('cmb_steel', '#4E535A', metallic=0.55, roughness=0.62),
        steel_dark=mat('cmb_steel_dark', '#33373C', metallic=0.50, roughness=0.70),
        rust=mat('cmb_rust', '#7E4430', metallic=0.05, roughness=0.90),
        foil=mat('cmb_foil', '#ABA79C', metallic=0.70, roughness=0.48),
        can_red=mat('cmb_can_red', '#9E4632', metallic=0.15, roughness=0.60),
        orange=mat('cmb_orange', '#D4822E', metallic=0.00, roughness=0.62),
        lamp=mat('cmb_lamp', '#D4822E', roughness=0.45,
                 emission='#FFB662', emit_strength=2.5),
        brass=mat('cmb_brass', '#8F7846', metallic=0.65, roughness=0.52),
        rubber=mat('cmb_rubber', '#232325', metallic=0.00, roughness=0.95),
        glass=mat('cmb_glass', '#8FA8B2', metallic=0.00, roughness=0.25, alpha=0.45),
        membrane=mat('cmb_membrane', '#BFB8A3', metallic=0.00, roughness=0.70, alpha=0.88),
        bone=mat('cmb_bone', '#AEAA9F', metallic=0.00, roughness=0.78),
    )


def reedfolk():
    """Reedfolk: grown, lashed, waxed, lacquered."""
    return dict(
        chitin=mat('reed_chitin', '#DCD2B8', metallic=0.00, roughness=0.55),
        amber=mat('reed_amber', '#C08E36', metallic=0.00, roughness=0.42),
        amber_clear=mat('reed_amber_clear', '#C08E36', metallic=0.00,
                        roughness=0.30, alpha=0.60),
        wax_green=mat('reed_wax_green', '#6A7440', metallic=0.00, roughness=0.70),
        honey=mat('reed_honey', '#4A3320', metallic=0.00, roughness=0.68),
        resin=mat('reed_resin', '#B8892F', metallic=0.00, roughness=0.38),
        glow=mat('reed_glow', '#8FC9A0', roughness=0.40,
                 emission='#A8E6BE', emit_strength=2.2),
        silk=mat('reed_silk', '#DED6C2', metallic=0.00, roughness=0.75),
        bark=mat('reed_bark', '#63503A', metallic=0.00, roughness=0.92),
        wing=mat('reed_wing', '#CFDCD6', metallic=0.00, roughness=0.35, alpha=0.38),
    )


def neutral():
    """Found objects and terrain. Neither tribe made these; they inherited them."""
    return dict(
        tarmac=mat('nt_tarmac', '#43443F', metallic=0.00, roughness=0.95),
        zinc=mat('nt_zinc', '#949890', metallic=0.60, roughness=0.55),
        steel_bright=mat('nt_steel_bright', '#B6BAB6', metallic=0.70, roughness=0.42),
        filter_paper=mat('nt_filter_paper', '#CFC2A0', metallic=0.00, roughness=0.86),
        filter_stain=mat('nt_filter_stain', '#836A44', metallic=0.00, roughness=0.88),
        match_wood=mat('nt_match_wood', '#C0A87C', metallic=0.00, roughness=0.84),
        match_head=mat('nt_match_head', '#A33A28', metallic=0.00, roughness=0.72),
        cap_paint=mat('nt_cap_paint', '#A24A38', metallic=0.10, roughness=0.62),
        pebble=mat('nt_pebble', '#8E8D85', metallic=0.00, roughness=0.92),
        pebble_pale=mat('nt_pebble_pale', '#ADACA2', metallic=0.00, roughness=0.90),
        grit=mat('nt_grit', '#605C52', metallic=0.00, roughness=0.95),
        algae=mat('nt_algae', '#5E6B36', metallic=0.00, roughness=0.88),
        algae_dry=mat('nt_algae_dry', '#8A7A46', metallic=0.00, roughness=0.90),
        ochre=mat('nt_ochre', '#B5822E', metallic=0.00, roughness=0.86),
        silt=mat('nt_silt', '#6B5B49', metallic=0.00, roughness=0.94),
        water_dark=mat('nt_water_dark', '#2F3A38', metallic=0.00, roughness=0.18),
    )
