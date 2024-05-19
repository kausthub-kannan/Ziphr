import ezkl
import os


class ZZK:
    def __init__(self):
        """
        Note:
            input.json is created as follows:
                x = test_data[0].reshape(1, 4)
                data_array = ((x).detach().numpy()).reshape([-1]).tolist()
                data = dict(input_data = [data_array])
                json.dump(data, open(data_path, 'w'))

            calibration.json is created as follows:
                calibration = dict(input_data = test_data.flatten().tolist())
                json.dump(calibration, open(calibration_path, 'w'))
        """
        # Required Inputs

        self.model_path = os.path.join("inputs/network.onnx")
        self.data_path = os.path.join('inputs/input.json')
        self.calibration_path = os.path.join('inputs/calibration.json')

        # ZKML Middleware Components
        self.compiled_model_path = os.path.join('outputs/network.ezkl')
        self.settings_path = os.path.join('outputs/settings.json')
        self.pk_path = os.path.join('outputs/test.pk')
        self.vk_path = os.path.join('outputs/test.vk')

    @staticmethod
    def set_visibility(input_visibility="private", weights_visibility="fixed", output_visibility="public"):
        run_args = ezkl.PyRunArgs()
        run_args.input_visibility = input_visibility
        run_args.param_visibility = weights_visibility
        run_args.output_visibility = output_visibility
        return run_args

    async def compile_model(self):
        ezkl.gen_settings(self.model_path, self.settings_path, py_run_args=self.set_visibility())
        ezkl.compile_circuit(self.model_path, self.compiled_model_path, self.settings_path)
        ezkl.get_srs(self.settings_path)
        ezkl.setup(
            self.compiled_model_path,
            self.vk_path,
            self.pk_path,
        )


if __name__ == '__main__':
    setup = ZZK()
    run_async(setup.compile_model())
