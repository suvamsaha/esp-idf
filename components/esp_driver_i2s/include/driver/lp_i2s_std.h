/*
 * SPDX-FileCopyrightText: 2015-2024 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#include "esp_types.h"
#include "esp_err.h"
#include "driver/i2s_types.h"
#include "hal/i2s_types.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Philips format in active slot that enabled by mask
 * @param bits_per_sample I2S data bit width
 * @param mono_or_stereo I2S_SLOT_MODE_MONO or I2S_SLOT_MODE_STEREO
 */
#define LP_I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(bits_per_sample, mono_or_stereo) { \
    .data_bit_width = (bits_per_sample), \
    .slot_bit_width = I2S_SLOT_BIT_WIDTH_AUTO, \
    .slot_mode = mono_or_stereo, \
    .slot_mask = I2S_STD_SLOT_BOTH, \
    .ws_width = bits_per_sample, \
    .ws_pol = false, \
    .bit_shift = true, \
    .left_align = true, \
    .big_endian = false, \
    .bit_order_lsb = false, \
}

/**
 * @brief MSB format in active slot enabled that by mask
 * @param bits_per_sample I2S data bit width
 * @param mono_or_stereo I2S_SLOT_MODE_MONO or I2S_SLOT_MODE_STEREO
 */
#define LP_I2S_STD_MSB_SLOT_DEFAULT_CONFIG(bits_per_sample, mono_or_stereo) { \
    .data_bit_width = (bits_per_sample), \
    .slot_bit_width = I2S_SLOT_BIT_WIDTH_AUTO, \
    .slot_mode = mono_or_stereo, \
    .slot_mask = I2S_STD_SLOT_BOTH, \
    .ws_width = bits_per_sample, \
    .ws_pol = false, \
    .bit_shift = false, \
    .left_align = true, \
    .big_endian = false, \
    .bit_order_lsb = false, \
}

/**
 * @brief PCM(short) format in active slot that enabled by mask
 * @param bits_per_sample I2S data bit width
 * @param mono_or_stereo I2S_SLOT_MODE_MONO or I2S_SLOT_MODE_STEREO
 */
#define LP_I2S_STD_PCM_SHORT_SLOT_DEFAULT_CONFIG(bits_per_sample, mono_or_stereo) { \
    .data_bit_width = (bits_per_sample), \
    .slot_bit_width = I2S_SLOT_BIT_WIDTH_AUTO, \
    .slot_mode = mono_or_stereo, \
    .slot_mask = I2S_STD_SLOT_BOTH, \
    .ws_width = 1, \
    .ws_pol = true, \
    .bit_shift = true, \
    .left_align = true, \
    .big_endian = false, \
    .bit_order_lsb = false, \
}

/**
 * @brief LP I2S pin configurations
 */
typedef struct {
    int bck;                               /*!< bck pin number */
    int ws;                                /*!< ws pin number */
    int din;                               /*!< din pin number */
} lp_i2s_std_gpio_config_t;

/**
 * @brief LP I2S slot configuration for standard mode
 */
typedef struct {
    /* General fields */
    i2s_data_bit_width_t    data_bit_width;     /*!< I2S sample data bit width (valid data bits per sample) */
    i2s_slot_bit_width_t    slot_bit_width;     /*!< I2S slot bit width (total bits per slot) */
    i2s_slot_mode_t         slot_mode;          /*!< Set mono or stereo mode with I2S_SLOT_MODE_MONO or I2S_SLOT_MODE_STEREO */

    /* Particular fields */
    i2s_std_slot_mask_t     slot_mask;          /*!< Select the left, right or both slot */
    uint32_t                ws_width;           /*!< WS signal width (i.e. the number of BCLK ticks that WS signal is high) */
    bool                    ws_pol;             /*!< WS signal polarity, set true to enable high lever first */
    bool                    bit_shift;          /*!< Set true to enable bit shift in Philips mode */
    bool                    left_align;         /*!< Set true to enable left alignment */
    bool                    big_endian;         /*!< Set true to enable big endian */
    bool                    bit_order_lsb;      /*!< Set true to enable lsb first */
} lp_i2s_std_slot_config_t;

/**
 * @brief LP I2S STD configuration
 */
typedef struct {
    lp_i2s_std_gpio_config_t    pin_cfg;    /*!< Pin configuration */
    lp_i2s_std_slot_config_t    slot_cfg;   /*!< STD mode slot configuration, can be generated by macros I2S_STD_[mode]_SLOT_DEFAULT_CONFIG, [mode] can be replaced with PHILIPS/MSB/PCM_SHORT/PCM_LONG */
    /* LP I2S only support slave mode, not support to configure the clock */
} lp_i2s_std_config_t;

/**
 * @brief Init LP I2S to STD mode
 *
 * @param[in] handle   LP I2S channel handle
 * @param[in] std_cfg  STD configuration
 *
 * @return
 *        - ESP_OK:                On success
 *        - ESP_ERR_INVALID_ARG:   Invalid argument
 *        - ESP_ERR_INVALID_STATE: Invalid state
 */
esp_err_t lp_i2s_channel_init_std_mode(lp_i2s_chan_handle_t handle, const lp_i2s_std_config_t *std_cfg);

#ifdef __cplusplus
}
#endif