import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    id: window
    width: 900
    height: 700
    visible: true
    title: "Questionnaire OCR - Desktop App"

    // Theme Colors
    property color primaryColor: "#2196F3"
    property color accentColor: "#FF4081"
    property color backgroundColor: "#F5F5F5"
    property color cardColor: "#FFFFFF"
    property color textColor: "#212121"
    property color textSecondaryColor: "#757575"

    background: Rectangle {
        color: window.backgroundColor
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Header Section
        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            Rectangle {
                width: 48
                height: 48
                radius: 24
                color: window.primaryColor

                Text {
                    anchors.centerIn: parent
                    text: "OCR"
                    color: "white"
                    font.bold: true
                    font.pixelSize: 16
                }
            }

            ColumnLayout {
                spacing: 2
                Text {
                    text: "Questionnaire OCR Desktop"
                    font.pixelSize: 22
                    font.bold: true
                    color: window.textColor
                }
                Text {
                    text: "Self-contained PySide6 QML Application sharing core image processing logic"
                    font.pixelSize: 13
                    color: window.textSecondaryColor
                }
            }
            Item { Layout.fillWidth: true }
        }

        // Main content (Split View: left side is image, right side is results)
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 20

            // Left Panel: Image Picker & Preview
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 450
                color: window.cardColor
                radius: 8
                border.color: "#E0E0E0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 15

                    Text {
                        text: "Form Image Source"
                        font.pixelSize: 16
                        font.bold: true
                        color: window.textColor
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "#FAFAFA"
                        radius: 6
                        border.color: "#EEEEEE"
                        border.width: 1
                        clip: true

                        Image {
                            id: previewImage
                            anchors.fill: parent
                            anchors.margins: 10
                            fillMode: Image.PreserveAspectFit
                            source: ""
                            visible: source != ""
                        }

                        ColumnLayout {
                            anchors.centerIn: parent
                            visible: previewImage.source == ""
                            spacing: 10

                            Text {
                                text: "No Image Selected"
                                font.pixelSize: 16
                                font.bold: true
                                color: window.textSecondaryColor
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Text {
                                text: "Select an image file of a questionnaire to start"
                                font.pixelSize: 12
                                color: "#BDBDBD"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10

                        Button {
                            text: "Choose Image..."
                            Layout.fillWidth: true
                            onClicked: fileDialog.open()
                        }

                        Button {
                            text: "Process Image"
                            Layout.fillWidth: true
                            highlighted: true
                            enabled: previewImage.source != ""

                            background: Rectangle {
                                color: parent.enabled ? (parent.down ? "#0B7dda" : window.primaryColor) : "#E0E0E0"
                                radius: 4
                            }

                            palette {
                                buttonText: "white"
                            }

                            onClicked: {
                                statusText.text = "Processing image using core logics..."
                                progressBar.visible = true
                                delayTimer.start()
                            }
                        }
                    }
                }
            }

            // Right Panel: Extracted Results
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 450
                color: window.cardColor
                radius: 8
                border.color: "#E0E0E0"
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 15

                    Text {
                        text: "Extracted Results"
                        font.pixelSize: 16
                        font.bold: true
                        color: window.textColor
                    }

                    ScrollView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true

                        TextArea {
                            id: resultsArea
                            placeholderText: "Extracted questionnaire fields and values will appear here..."
                            placeholderTextColor: window.textSecondaryColor
                            readOnly: true
                            font.family: "Courier New"
                            font.pixelSize: 13
                            background: null
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: "#EEEEEE"
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10

                        Button {
                            text: "Clear"
                            enabled: resultsArea.text != ""
                            onClicked: {
                                resultsArea.text = ""
                                statusText.text = "Cleared results."
                            }
                        }

                        Button {
                            text: "Copy to Clipboard"
                            Layout.fillWidth: true
                            enabled: resultsArea.text != ""
                            onClicked: {
                                resultsArea.selectAll()
                                resultsArea.copy()
                                statusText.text = "Results copied to clipboard!"
                            }
                        }
                    }
                }
            }
        }

        // Status & Progress Bar
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            ProgressBar {
                id: progressBar
                Layout.fillWidth: true
                indeterminate: true
                visible: false
            }

            Text {
                id: statusText
                text: "Ready"
                font.pixelSize: 12
                color: window.textSecondaryColor
            }
        }
    }

    FileDialog {
        id: fileDialog
        title: "Select Questionnaire Image"
        nameFilters: ["Images (*.png *.jpg *.jpeg *.bmp)"]
        onAccepted: {
            previewImage.source = selectedFile
            resultsArea.text = ""
            statusText.text = "Selected: " + selectedFile
        }
    }

    Timer {
        id: delayTimer
        interval: 100 // Minimal delay to show UI updates
        repeat: false
        onTriggered: {
            var result = formProcessor.processImage(previewImage.source.toString())
            progressBar.visible = false
            if (result.error !== undefined) {
                resultsArea.text = "Error processing image:\n" + result.error
                statusText.text = "Failed!"
            } else {
                resultsArea.text = JSON.stringify(result, null, 4)
                statusText.text = "Extraction completed successfully!"
            }
        }
    }
}
