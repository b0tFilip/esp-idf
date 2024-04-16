/*
 * SPDX-FileCopyrightText: 2023-2024 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#include <stdint.h>
#include "soc/clk_tree_defs.h"
#include "esp_assert.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief MIPI DSI Data Type (DT)
 */
typedef enum {
    MIPI_DSI_DT_VSYNC_START = 0x01,                 /*!< V Sync Start */
    MIPI_DSI_DT_VSYNC_END = 0x11,                   /*!< V Sync End */
    MIPI_DSI_DT_HSYNC_START = 0x21,                 /*!< H Sync Start */
    MIPI_DSI_DT_HSYNC_END = 0x31,                   /*!< H Sync End */
    MIPI_DSI_DT_EOT_PACKET = 0x08,                  /*!< End of Transmission */
    MIPI_DSI_DT_COLOR_MODE_OFF = 0x02,              /*!< Color Mode Off */
    MIPI_DSI_DT_COLOR_MODE_ON = 0x12,               /*!< Color Mode On */
    MIPI_DSI_DT_SHUTDOWN_PERIPHERAL = 0x22,         /*!< Shutdown Peripheral */
    MIPI_DSI_DT_TURN_ON_PERIPHERAL = 0x32,          /*!< Turn On Peripheral */
    MIPI_DSI_DT_GENERIC_SHORT_WRITE_0 = 0x03,       /*!< Generic Short Write, with no parameter */
    MIPI_DSI_DT_GENERIC_SHORT_WRITE_1 = 0x13,       /*!< Generic Short Write, with 1 byte parameter */
    MIPI_DSI_DT_GENERIC_SHORT_WRITE_2 = 0x23,       /*!< Generic Short Write, with 2 byte parameter */
    MIPI_DSI_DT_GENERIC_READ_REQUEST_0 = 0x04,      /*!< Generic Read Request, with no parameter */
    MIPI_DSI_DT_GENERIC_READ_REQUEST_1 = 0x14,      /*!< Generic Read Request, with 1 byte parameter */
    MIPI_DSI_DT_GENERIC_READ_REQUEST_2 = 0x24,      /*!< Generic Read Request, with 2 byte parameter */
    MIPI_DSI_DT_DCS_SHORT_WRITE_0 = 0x05,           /*!< DCS Short Write, with no parameter */
    MIPI_DSI_DT_DCS_SHORT_WRITE_1 = 0x15,           /*!< DCS Short Write, with 1 byte parameter */
    MIPI_DSI_DT_DCS_READ_0 = 0x06,                  /*!< DCS Read, with no parameter */
    MIPI_DSI_DT_SET_MAXIMUM_RETURN_PKT = 0x37,      /*!< Set Maximum Return Packet Size */
    MIPI_DSI_DT_NULL_PACKET = 0x09,                 /*!< Null Packet, no data */
    MIPI_DSI_DT_BLANKING_PACKET = 0x19,             /*!< Blanking Packet, no data */
    MIPI_DSI_DT_GENERIC_LONG_WRITE = 0x29,          /*!< Generic Long Write */
    MIPI_DSI_DT_DCS_LONG_WRITE = 0x39,              /*!< DCS Long Write */
    MIPI_DSI_DT_PACKED_PIXEL_STREAM_RGB_16 = 0x0E,  /*!< Packed Pixel Stream, RGB565 */
    MIPI_DSI_DT_PACKED_PIXEL_STREAM_RGB_18 = 0x1E,  /*!< Packed Pixel Stream, RGB666 */
    MIPI_DSI_DT_LOOSELY_PIXEL_STREAM_RGB_18 = 0x2E, /*!< Loosely Pixel Stream, RGB666 */
    MIPI_DSI_DT_PACKED_PIXEL_STREAM_RGB_24 = 0x3E,  /*!< Packed Pixel Stream, RGB888 */
} __attribute__((packed)) mipi_dsi_data_type_t;

/**
 * @brief The kind of test pattern that can be generated by the DSI Host controller
 */
typedef enum {
    MIPI_DSI_PATTERN_NONE,           /*!< No pattern */
    MIPI_DSI_PATTERN_BAR_VERTICAL,   /*!< Vertical BAR pattern, with different colors */
    MIPI_DSI_PATTERN_BAR_HORIZONTAL, /*!< Horizontal BAR pattern, with different colors */
    MIPI_DSI_PATTERN_BER_VERTICAL,   /*!< Vertical Bit Error Rate(BER) pattern */
} mipi_dsi_pattern_type_t;

#if SOC_MIPI_DSI_SUPPORTED
/**
 * @brief MIPI DSI PHY clock source
 */
typedef soc_periph_mipi_dsi_phy_clk_src_t mipi_dsi_phy_clock_source_t;

/**
 * @brief MIPI DSI DPI clock source
 */
typedef soc_periph_mipi_dsi_dpi_clk_src_t mipi_dsi_dpi_clock_source_t;
#else
typedef int mipi_dsi_phy_clock_source_t;
typedef int mipi_dsi_dpi_clock_source_t;
#endif // SOC_MIPI_DSI_SUPPORTED

#ifdef __cplusplus
}
#endif