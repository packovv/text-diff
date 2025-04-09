package com.textdiff.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.textdiff.DiffResult
import com.textdiff.TextDiff

@Composable
fun TextDiffScreen() {
    var text1 by remember { mutableStateOf("") }
    var text2 by remember { mutableStateOf("") }
    var diffResult by remember { mutableStateOf<DiffResult?>(null) }
    val textDiff = remember { TextDiff() }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Текстовые поля для ввода
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            TextField(
                value = text1,
                onValueChange = { text1 = it },
                label = { Text("Первый текст") },
                modifier = Modifier.weight(1f)
            )
            
            TextField(
                value = text2,
                onValueChange = { text2 = it },
                label = { Text("Второй текст") },
                modifier = Modifier.weight(1f)
            )
        }
        
        // Кнопка сравнения
        Button(
            onClick = {
                kotlinx.coroutines.MainScope().launch {
                    diffResult = textDiff.compare(text1, text2)
                }
            },
            modifier = Modifier.align(Alignment.End)
        ) {
            Text("Сравнить")
        }
        
        // Результаты сравнения
        diffResult?.let { result ->
            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                items(result.removed) { line ->
                    Text(
                        text = "- $line",
                        color = Color.Red,
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color.Red.copy(alpha = 0.1f))
                            .padding(4.dp)
                    )
                }
                
                items(result.unchanged) { line ->
                    Text(
                        text = "  $line",
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(4.dp)
                    )
                }
                
                items(result.added) { line ->
                    Text(
                        text = "+ $line",
                        color = Color.Green,
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color.Green.copy(alpha = 0.1f))
                            .padding(4.dp)
                    )
                }
            }
        }
    }
} 