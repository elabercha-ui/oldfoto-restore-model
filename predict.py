from typing import Any, Dict
from pathlib import Path

from cog import BasePredictor, Input, Path as CogPath


def run_workflow(image_path: Path, params: Dict[str, Any]) -> Path:
    """
    Здесь позже должен быть настоящий код,
    который запускает твой workflow и возвращает путь к результату.

    Сейчас это заглушка, чтобы модель на Replicate могла собраться.
    """
    raise NotImplementedError("Workflow runner is not connected yet.")


class Predictor(BasePredictor):
    def predict(
        self,
        # --- основной вход ---
        image: CogPath = Input(description="Input portrait image"),

        # --- размер ---
        turn_on_edit_size: bool = Input(
            default=True, description="Turn on custom resize"
        ),
        fill_new_size: int = Input(
            default=1536, ge=256, le=4096, description="New size (pixels)"
        ),

        # --- основные режимы восстановления / flux / апскейл ---
        enable_face_restore: bool = Input(default=False),
        face_restore_by_contour: bool = Input(default=False),
        detail_restore_by_contour: bool = Input(default=False),
        face_restore_method_2: bool = Input(default=False),
        detail_restore_method_2: bool = Input(default=False),
        keep_original_face_flux: bool = Input(default=False),
        enable_flux: bool = Input(default=False),
        enable_upscale: bool = Input(default=False),
        smooth_face: bool = Input(default=False),

        # --- слайдеры качества / деформаций / цвета ---
        face_resemblance: float = Input(
            default=0.56, ge=0.0, le=1.0
        ),
        detail_resemblance: float = Input(
            default=0.45, ge=0.0, le=1.0
        ),
        face_deformity_level: float = Input(
            default=1.0, ge=0.0, le=1.0
        ),
        detail_deformity_level: float = Input(
            default=1.0, ge=0.0, le=1.0
        ),
        noise_level: float = Input(
            default=0.02, ge=0.0, le=1.0
        ),
        smoothness_of_face: int = Input(
            default=100, ge=0, le=100
        ),
        flux_impact_level: float = Input(
            default=0.25, ge=0.0, le=1.0
        ),
        upscale_level: int = Input(
            default=2, ge=1, le=8
        ),
        face_color_level: float = Input(
            default=0.95, ge=0.0, le=1.0
        ),
        detail_color_level: float = Input(
            default=0.95, ge=0.0, le=1.0
        ),
        blur_face_level: float = Input(
            default=2.0, ge=0.0, le=10.0
        ),
        blur_detail_level: float = Input(
            default=2.0, ge=0.0, le=10.0
        ),

        # --- предпросмотр / сравнение / доп.режимы ---
        turn_on_image_preview: bool = Input(default=False),
        compare_images: bool = Input(default=False),
        prompt_your_language: bool = Input(
            default=True, description="Use prompt in your language"
        ),
        blend_images: bool = Input(default=True),
        get_detail_face_image: bool = Input(default=False),

        # --- кроп / цветовая панель ---
        enable_crop_image: bool = Input(default=False),
        crop_code: int = Input(
            default=1, ge=0, le=9, description="Crop preset code"
        ),
        color_panel: bool = Input(default=False),

        # --- топаз / фотошоп (для будущей интеграции, сейчас в облаке не работают) ---
        enable_topaz: bool = Input(
            default=False,
            description="Local Topaz integration (has no effect on Replicate for now)",
        ),
        photoshop_original_img: bool = Input(
            default=False,
            description="Photoshop original image (local only, no effect on Replicate)",
        ),
        photoshop_result_image: bool = Input(
            default=False,
            description="Photoshop result image (local only, no effect on Replicate)",
        ),

        # --- текст ---
        prompt_text: str = Input(
            default="",
            description="Optional text prompt for guidance",
        ),
        watermark_text: str = Input(
            default="",
            description="Watermark text to add on image",
        ),
    ) -> CogPath:
        """
        Точка входа для Replicate:
        собираем все параметры в словарь и передаём в раннер.
        """

        params: Dict[str, Any] = {
            "turn_on_edit_size": turn_on_edit_size,
            "fill_new_size": fill_new_size,
            "enable_face_restore": enable_face_restore,
            "face_restore_by_contour": face_restore_by_contour,
            "detail_restore_by_contour": detail_restore_by_contour,
            "face_restore_method_2": face_restore_method_2,
            "detail_restore_method_2": detail_restore_method_2,
            "keep_original_face_flux": keep_original_face_flux,
            "enable_flux": enable_flux,
            "enable_upscale": enable_upscale,
            "smooth_face": smooth_face,
            "face_resemblance": face_resemblance,
            "detail_resemblance": detail_resemblance,
            "face_deformity_level": face_deformity_level,
            "detail_deformity_level": detail_deformity_level,
            "noise_level": noise_level,
            "smoothness_of_face": smoothness_of_face,
            "flux_impact_level": flux_impact_level,
            "upscale_level": upscale_level,
            "face_color_level": face_color_level,
            "detail_color_level": detail_color_level,
            "blur_face_level": blur_face_level,
            "blur_detail_level": blur_detail_level,
            "turn_on_image_preview": turn_on_image_preview,
            "compare_images": compare_images,
            "prompt_your_language": prompt_your_language,
            "blend_images": blend_images,
            "get_detail_face_image": get_detail_face_image,
            "enable_crop_image": enable_crop_image,
            "crop_code": crop_code,
            "color_panel": color_panel,
            "enable_topaz": enable_topaz,
            "photoshop_original_img": photoshop_original_img,
            "photoshop_result_image": photoshop_result_image,
            "prompt_text": prompt_text,
            "watermark_text": watermark_text,
        }

        output_path = run_workflow(Path(image), params)
        return CogPath(output_path)
