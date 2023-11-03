from PySide6.QtCore import (
    Signal,
    Slot,
    Property,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    Qt,
    QEasingCurve,
    QPoint,
    QSize,
    QRectF,
    QPointF,
)
from PySide6.QtGui import (
    QColor,
    QBrush,
    QPen,
    QPaintEvent,
    QPainter,
)
from PySide6.QtWidgets import QCheckBox


class AnimCheckBox(QCheckBox):
    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(
        self,
        parent=None,
        bar_color=Qt.GlobalColor.gray,
        checked_color="#23d18b",
        handle_color=Qt.GlobalColor.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE",
    ):
        super().__init__(parent)

        self.bar_brush = QBrush(bar_color)
        self.bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self.handle_brush = QBrush(handle_color)
        self.handle_checked_brush = QBrush(QColor(checked_color))

        self.pulse_unchecked_brush = QBrush(QColor(pulse_unchecked_color))
        self.pulse_checked_brush = QBrush(QColor(pulse_checked_color))

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        self._pulse_radius = 0

        self.check_animation = QPropertyAnimation(self, b"handle_position", self)
        self.check_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.check_animation.setDuration(200)

        self.pulse_animation = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_animation.setDuration(250)
        self.pulse_animation.setStartValue(10)
        self.pulse_animation.setEndValue(20)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.check_animation)
        self.animation_group.addAnimation(self.pulse_animation)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Slot(int)
    def setup_animation(self, value):
        self.animation_group.stop()
        if value:
            self.check_animation.setEndValue(1)
        else:
            self.check_animation.setEndValue(0)
        self.animation_group.start()

    def paintEvent(self, e: QPaintEvent) -> None:
        rect = self.contentsRect()
        handle_r = round(0.3 * rect.height())  # handle radius
        bar_rect = QRectF(0, 0, rect.width() - handle_r * 2, 0.4 * rect.height())
        bar_rect.moveCenter(rect.center())
        rounding = bar_rect.height() / 2
        trail_len = rect.width() - 2 * handle_r  # handle path
        
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(self._transparent_pen)

        xpos = rect.x() + handle_r + trail_len * self._handle_position
        if self.pulse_animation.state() == QPropertyAnimation.State.Running:
            p.setBrush(
                self.pulse_checked_brush
                if self.isChecked()
                else self.pulse_unchecked_brush
            )
            p.drawEllipse(
                QPointF(xpos, bar_rect.center().y()),
                self._pulse_radius,
                self._pulse_radius,
            )

        if self.isChecked():
            p.setBrush(self.bar_checked_brush)
            p.drawRoundedRect(bar_rect, rounding, rounding)
            p.setBrush(self.handle_checked_brush)
        else:
            p.setBrush(self.bar_brush)
            p.drawRoundedRect(bar_rect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self.handle_brush)

        p.drawEllipse(QPointF(xpos, bar_rect.center().y()), handle_r, handle_r)

        p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, value):
        self._handle_position = value
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, value):
        self._pulse_radius = value
        self.update()
