r"""
Filtered Hopf algebras with basis
"""
#*****************************************************************************
#  Copyright (C) 2017 Travis Scrimshaw <tcscrims at gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.categories.category_with_axiom import CategoryWithAxiom_over_base_ring
from sage.categories.tensor import tensor
from sage.categories.filtered_modules import FilteredModulesCategory
from sage.categories.with_realizations import WithRealizationsCategory
from sage.misc.cachefunc import cached_method

import six


class FilteredHopfAlgebrasWithBasis(FilteredModulesCategory):
    """
    The category of filtered Hopf algebras with a distinguished basis.

    The basis is assumed to "respect the filtration," in the sense
    that it satisfies the requirements of
    :class:`FilteredModulesWithBasis`.

    EXAMPLES::

        sage: C = HopfAlgebrasWithBasis(ZZ).Filtered(); C
        Category of filtered hopf algebras with basis over Integer Ring
        sage: C.super_categories()
        [Category of hopf algebras with basis over Integer Ring,
         Category of filtered algebras with basis over Integer Ring]

        sage: C is HopfAlgebras(ZZ).WithBasis().Filtered()
        True
        sage: C is HopfAlgebras(ZZ).Filtered().WithBasis()
        False

    TESTS::

        sage: TestSuite(C).run()
    """
    class WithRealizations(WithRealizationsCategory):
        @cached_method
        def super_categories(self):
            """
            EXAMPLES::

                sage: HopfAlgebrasWithBasis(QQ).Filtered().WithRealizations().super_categories()
                [Join of Category of hopf algebras over Rational Field
                     and Category of filtered algebras over Rational Field]

            TESTS::

                sage: TestSuite(HopfAlgebrasWithBasis(QQ).Filtered().WithRealizations()).run()
            """
            from sage.categories.hopf_algebras import HopfAlgebras
            R = self.base_category().base_ring()
            return [HopfAlgebras(R).Filtered()]


    class Connected(CategoryWithAxiom_over_base_ring):
        class ParentMethods:
            @cached_method
            def antipode_on_basis(self, index):
                r"""
                The antipode on the basis element indexed by ``index``.

                INPUT:

                - ``index`` -- an element of the index set

                For a filtered connected Hopf algebra, we can define
                an antipode recursively by

                .. MATH::

                    S(x) := -\sum_{x^L \neq x} S(x^L) \times x^R + \epsilon(x)

                in general or `x` if `|x| = 0`.

                TESTS::

                    sage: H = GradedHopfAlgebrasWithBasis(QQ).Connected().example()
                    sage: H.monomial(0).antipode() # indirect doctest
                    P0
                    sage: H.monomial(1).antipode() # indirect doctest
                    -P1
                    sage: H.monomial(2).antipode() # indirect doctest
                    P2
                    sage: H.monomial(3).antipode() # indirect doctest
                    -P3
                """
                if self.monomial(index) == self.one():
                    return self.one()

                S = self.antipode_on_basis
                x__S_Id = tensor([self, self]).module_morphism(
                    lambda ab: S(ab[0]) * self.monomial(ab[1]),
                    codomain=self)
                smi = self.monomial(index)
                return -x__S_Id(smi.coproduct()
                                - tensor([smi, self.one()])
                               ) + smi.counit()

            def antipode(self, elem):
                r"""
                Return the antipode of ``self`` applied to ``elem``.

                TESTS::

                    sage: H = GradedHopfAlgebrasWithBasis(QQ).Connected().example()
                    sage: H.antipode(H.monomial(140))
                    P140

                    sage: H.monomial(0).antipode()
                    P0
                    sage: H.monomial(2).antipode()
                    P2
                    sage: (2*H.monomial(1) + 3*H.monomial(4)).antipode()
                    -2*P1 + 3*P4
                """
                return self.linear_combination(
                    (self.antipode_on_basis(mon), coeff)
                    for mon, coeff in six.iteritems(elem.monomial_coefficients(copy=False))
                )

        class ElementMethods:
            pass

