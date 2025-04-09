package com.textdiff

import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import com.textdiff.ui.TextDiffScreen

fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        title = "Text Diff Tool"
    ) {
        TextDiffScreen()
    }
} 