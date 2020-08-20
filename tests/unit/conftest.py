# pylint: disable=redefined-outer-name
import logging

import pytest

from expertsystem import ui
from expertsystem.amplitude.canonical_decay import CanonicalAmplitudeGenerator
from expertsystem.amplitude.helicity_decay import HelicityAmplitudeGenerator
from expertsystem.data import ParticleCollection
from expertsystem.state.particle import DATABASE
from expertsystem.ui import (
    InteractionTypes,
    StateTransitionManager,
)


logging.basicConfig(level=logging.ERROR)


@pytest.fixture(scope="package")
def particle_database() -> ParticleCollection:
    ui.load_default_particle_list()
    return DATABASE


@pytest.fixture(scope="module")
def jpsi_to_gamma_pi_pi_canonical_solutions():
    stm = StateTransitionManager(
        initial_state=[("J/psi(1S)", [-1, 1])],
        final_state=["gamma", "pi0", "pi0"],
        allowed_intermediate_particles=["f(0)"],
        formalism_type="canonical-helicity",
    )
    stm.set_allowed_interaction_types([InteractionTypes.EM])
    graph_interaction_settings_groups = stm.prepare_graphs()
    solutions, _ = stm.find_solutions(graph_interaction_settings_groups)
    return solutions


@pytest.fixture(scope="module")
def jpsi_to_gamma_pi_pi_helicity_solutions():
    stm = StateTransitionManager(
        initial_state=[("J/psi(1S)", [-1, 1])],
        final_state=["gamma", "pi0", "pi0"],
        allowed_intermediate_particles=["f(0)"],
    )
    stm.set_allowed_interaction_types(
        [InteractionTypes.Strong, InteractionTypes.EM]
    )
    graph_interaction_settings_groups = stm.prepare_graphs()
    solutions, _ = stm.find_solutions(graph_interaction_settings_groups)
    return solutions


@pytest.fixture(scope="module")
def jpsi_to_gamma_pi_pi_canonical_amplitude_generator(
    jpsi_to_gamma_pi_pi_canonical_solutions,
):
    amplitude_generator = CanonicalAmplitudeGenerator()
    amplitude_generator.generate(jpsi_to_gamma_pi_pi_canonical_solutions)
    return amplitude_generator


@pytest.fixture(scope="module")
def jpsi_to_gamma_pi_pi_helicity_amplitude_generator(
    jpsi_to_gamma_pi_pi_helicity_solutions,
):
    amplitude_generator = HelicityAmplitudeGenerator()
    amplitude_generator.generate(jpsi_to_gamma_pi_pi_helicity_solutions)
    return amplitude_generator