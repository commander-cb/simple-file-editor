import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, QWidget
from moviepy.editor import concatenate_videoclips, VideoFileClip


class VideoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Video Editor")
        self.setGeometry(200, 200, 600, 400)
        self.video_list = []

        # Main layout
        layout = QVBoxLayout()

        # File list widget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Buttons
        self.add_button = QPushButton("Add AVI Files")
        self.add_button.clicked.connect(self.add_files)
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        layout.addWidget(self.remove_button)

        self.export_button = QPushButton("Export to MP4")
        self.export_button.clicked.connect(self.export_videos)
        layout.addWidget(self.export_button)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select AVI Files", "", "AVI Files (*.avi)")
        if files:
            self.video_list.extend(files)
            self.list_widget.addItems(files)

    def remove_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.video_list.remove(item.text())
            self.list_widget.takeItem(self.list_widget.row(item))

    def export_videos(self):
        if not self.video_list:
            QMessageBox.warning(self, "Warning", "No videos to export!")
            return

        output_file, _ = QFileDialog.getSaveFileName(self, "Save MP4 File", "", "MP4 Files (*.mp4)")
        if not output_file:
            return

        try:
            clips = [VideoFileClip(video) for video in self.video_list]
            final_clip = concatenate_videoclips(clips, method="compose")
            final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
            QMessageBox.information(self, "Success", f"Video exported to {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = VideoEditor()
    editor.show()
    sys.exit(app.exec_())
