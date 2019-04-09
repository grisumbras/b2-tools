from conans import (
    ConanFile,
    python_requires,
    tools,
)
import os
import re


b2 = python_requires("b2-helper/0.2.0@grisumbras/testing")


def get_version():
    try:
        content = tools.load("jamroot.jam")
        match = re.search(r"constant\s*VERSION\s*:\s*(\S+)\s*;", content)
        return match.group(1)
    except:
        pass


class EnumFlagsConan(b2.B2.Mixin, ConanFile):
    name = "b2-tools"
    version = get_version()
    description = "Helper tools for Boost.Build"
    topics = "building",
    author = "Dmitry Arkhipov <grisumbras@gmail.com>"
    license = "BSL-1.0"
    url = "https://gitlab.com/grisumbras/b2-tools"
    homepage = url

    exports_sources = (
        "jamroot.jam",
        "modules/*.jam",
        "LICENSE*",
    )
    no_copy_source = True
    build_requires = "boost_build/[>=1.68]@bincrafters/stable"

    def b2_setup_builder(self, builder):
        builder.properties.install_prefix = self.package_folder
        return builder

    def package_info(self):
        self.info.header_only()

        if self.in_local_cache:
            module_dir = os.path.join(
                self.package_folder, "share", "boost-build", "contrib",
            )
        else:
            module_dir = os.path.join(os.path.dirname(__file__), "modules")

        self.env_info.BOOST_BUILD_PATH.append(module_dir)
